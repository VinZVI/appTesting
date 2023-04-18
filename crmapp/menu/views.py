from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from crmapp.db import db
from crmapp.exceptions import DBSaveException, DataBaseSaveError
from crmapp.hookahs.models import Hookah
from crmapp.menu.forms import CategoryForm, CategoryDeleteForm, ItemForm, ItemDeleteForm
from crmapp.menu.models import Category, Item
from crmapp.user.decorators import manager_required



blueprint = Blueprint('menu', __name__, url_prefix='/menu')


@blueprint.route("/<name_hookah>")
@login_required
def menu(name_hookah):
    title = name_hookah
    hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
    categories_list = hookah.categories.all()
    items_list = Item.query.filter(Item.hookah_id == hookah.id, Item.category_id, Item.user_id).all()
    return render_template(
        "menu/menu.html",
        page_title=title,
        categories_list=categories_list,
        items_list=items_list
    )

@blueprint.route("/menu-edit/<name_hookah>")
@manager_required
def menu_edit(name_hookah):
    title = name_hookah
    hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
    categories_list = hookah.categories.all()
    items_list = Item.query.filter(Item.hookah_id == hookah.id, Item.category_id, Item.user_id).all()
    form1 = CategoryForm()
    form2 = ItemForm()
    return render_template(
        "menu/menu-edit.html",
        page_title=title,
        categories_list=categories_list,
        items_list=items_list
        form1=form1
        form2=form2
    )

@blueprint.route("/menu-edit/<name_hookah>/add-category", methods=['POST'])
@manager_required
def add_category(name_hookah):
    form = CategoryForm(request.form)
    if form.validate_on_submit:
        user = current_user._get_current_object()
        current_hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        new_category = Category(
            category_name = form.category_name.data,
            category_description = form.category_description.data
            hookah_id = current_hookah.id
            user_id = user.id
        )
        db.session.add(new_category)
        try:
            db.seesion.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили категорию {form.category_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Вы попытались создать категорию {form.category_name.data}, \
    которая уже существует, выберете другое название')
    return redirect(url_for('menu.menu-edit'))

@blueprint.route("/menu-edit/<name_hookah>/delete-category", methods=['GET', 'DELETE'])
@manager_required
def delete_category(name_hookah, category_name):
    form = CategoryDeleteForm(request.form)
    if request.method == 'DELETE' and form.validate_on_submit():
        hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        category = Category.query.filter_by(Category.hookah_id == hookah.id, category_name=category_name).first()
        db.session.delete(category)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы удалили категорию {category_name}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Такой категории {category_name} не существует')
    return redirect('menu.menu-edit')


@blueprint.route("/menu-edit/<name_hookah>/add-item", methods=['POST'])
@manager_required
def add_item(name_hookah, category_name):
    form = ItemForm(request.form)
    if form.validate_on_submit:
        user = current_user._get_current_object()
        current_hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        current_category = Category.query.filter_by(category_name=category_name).first()
        new_item = Item(
            item_name = form.item_name.data
            item_description = form.item_description.data
            price = form.price.data
            availability = form.availability.data
            category_id = current_category.id
            hookah_id = current_hookah.id
            user_id = user.id
        )
        db.session.add(new_item)
        try:
            db.seesion.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили позицию {form.item_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Вы попытались создать позицию {form.item_name.data}, \
    которая уже существует, выберете другое название')
    return redirect(url_for('menu.menu-edit'))

@blueprint.route("/menu-edit/<name_hookah>", methods=['GET', 'DELETE'])
@manager_required
def delete_item(name_hookah, category_name, item_name):
    form = ItemDeleteForm(request.form)
    if request.method == 'DELETE' and form.validate_on_submit():
        hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        current_category = Category.query.filter_by(category_name=category_name).first()
        item = Item.query.filter(Item.category_id == current_category.id, Item.hookah_id == hookah.id).first()
        db.session.delete(item)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы удалили позицию {item_name}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Такой позиции {item_name} не существует')
    return redirect('menu.menu-edit')