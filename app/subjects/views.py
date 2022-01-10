from flask import render_template, redirect, url_for
from .forms import CreateSubjectForm
from . import sub_blueprint
from .models import Subject
from .. import db


@sub_blueprint.route('/', methods=['GET', 'POST'])
def subjects():
    subject = Subject.query.order_by(Subject.id.desc())
    return render_template('subjects.html', subjects=subject)


@sub_blueprint.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    subject = Subject.query.get_or_404(id)
    return render_template('detail_sub.html', subject=subject)


@sub_blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    subject = Subject.query.get_or_404(id)

    db.session.delete(subject)
    db.session.commit()

    return redirect(url_for('.subjects'))


@sub_blueprint.route('/create', methods=['GET', 'POST'])
def subject_create():
    form = CreateSubjectForm()
    if form.validate_on_submit():
        subject = Subject(name_subject=form.name_subject.data, teacher=form.teacher.data, specialty=form.specialty.data,
                          semester=form.semester.data, type_occupation=form.type_occupation.data,
                          control=form.control.data)

        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('sub.subjects'))

    return render_template('subject_create.html', form=form)


@sub_blueprint.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    subject = Subject.query.get_or_404(id)

    form = CreateSubjectForm()

    if form.validate_on_submit():
        subject.name_subject = form.name_subject.data
        subject.teacher = form.teacher.data
        subject.specialty = form.specialty.data
        subject.semester = form.semester.data
        subject.type_occupation = form.type_occupation.data
        subject.control = subject.control.data

        db.session.add(subject)
        db.session.commit()

        return redirect(url_for('.detail', id=id))

    form.name_subject.data = subject.name_subject
    form.teacher.data = subject.teacher
    form.specialty.data = subject.specialty
    form.semester.data = subject.semester
    form.type_occupation.data = subject.type_occupation
    subject.control.data = subject.control

    return render_template('update.html', form=form)
