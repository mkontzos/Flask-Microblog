from datetime import datetime
from turtle import tilt
from types import MethodDescriptorType
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from sqlalchemy import null
from app import db
from app.forum.forms import AnswerForm, QuestionForm, CategoryForm, EmptyForm
from app.models import Answer, User, Question, Category, Post, Message, Notification
from app.translate import translate
from app.forum import bp

@bp.route('/forum/index')
def index():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(Question.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('forum.index', page=questions.next_num) \
        if questions.has_next else None
    prev_url = url_for('forum.index', page=questions.prev_num) \
        if questions.has_prev else None
    return render_template('forum/index.html',title=_('Forum'),
                           questions=questions.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/forum/question/ask', methods=['GET', 'POST'])
def ask_question():
    form = QuestionForm()
    form.category.choices = [(c.id, c.title) for c in Category.query.order_by('title')]
    if form.validate_on_submit():
        try:
            language = detect(form.body.data)
        except LangDetectException:
            language = ''
        
        question = Question(title=form.title.data, body=form.body.data,
                                category=form.category.data, language=language,
                                user_id = current_user.is_authenticated and current_user.id or None)

        db.session.add(question)
        db.session.commit()
        flash(_('Your question is now live!'))
        return redirect(url_for('forum.index'))
    return render_template('forum/question_post.html', title=_('Forum'), form=form)

@bp.route('/forum/question/<title>')
def question_details(title):
    question = Question.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    answers = question.answers.order_by(Answer.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('forum.question_details', username=user.username,
                       page=answers.next_num) if answers.has_next else None
    prev_url = url_for('forum.question_details', username=user.username,
                       page=answers.prev_num) if answers.has_prev else None
    form = EmptyForm()
    return render_template('forum/question_details.html', question=question, 
                            answer_list = answers.items,next_url=next_url, 
                            prev_url=prev_url, form=form)


@bp.route('/forum/question/<title>/<id>/answer', methods=['GET', 'POST'])
def answer_question(title,id):
    form = AnswerForm()
    if form.validate_on_submit():
        try:
            language = detect(form.body.data)
        except LangDetectException:
            language = ''
        answer = Answer(body=form.body.data,user_id=current_user.id,language=language, question_id=id)
        db.session.add(answer)
        db.session.commit()
        flash(_('Your answer is now live!'))
        return redirect(url_for('forum.question_details', title=title))
    return render_template('forum/answer.html', title=_('Answer question'), form=form)

@bp.route('/forum/categories')
@login_required
def view_categories():
    existing_categories = Category.query.all()
    if existing_categories is null:
        return redirect(url_for('forum.index'))
    return render_template('forum/categories_list.html', title=_('Categories list'),
                            existing_categories=existing_categories)

@bp.route('/forum/category/create', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    existing_categories = Category.query.all()
    if form.validate_on_submit():
        try:
            language = detect(form.title.data)
        except LangDetectException:
            language = ''
        for category in existing_categories:
            if category.title == form.title.data:
                flash(_('The category already exists!'))
                return redirect(url_for('forum.index'))
        category = Category(title=form.title.data)
        db.session.add(category)
        db.session.commit()
        flash(_('The category has been created.'))
        return redirect(url_for('forum.index'))
    return render_template('forum/category_post.html', title=_('Create category'),
                            existing_categories=existing_categories, form=form)

@bp.route('/forum/category/<title>')
def category_questions(title):
    page = request.args.get('page', 1, type=int)
    category_from_db = Category.query.filter_by(title=title).first_or_404()
    questions = Question.query.filter_by(category=category_from_db.id).order_by(Question.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('forum.category_questions', page=questions.next_num) \
        if questions.has_next else None
    prev_url = url_for('forum.category_questions', page=questions.prev_num) \
        if questions.has_prev else None
    return render_template('forum/answer_per_category.html',title=_('Forum'),
                           questions=questions.items, next_url=next_url,
                           prev_url=prev_url, page_title=title, id=category_from_db.id)

@bp.route('/forum/category/delete/<id>')
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id).delete()
    db.session.commit()
    flash(_('The category has been deleted.'))
    return redirect(url_for('forum.view_categories'))
        