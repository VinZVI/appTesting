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
    items_list = Item.query.filter(Item.hookah_id == hookah.id, Item.category_id).all()
    category_form = CategoryForm()
    item_form = ItemForm()
    return render_template(
        "menu/menu-edit.html",
        title=title,
        categories_list=categories_list,
        items_list=items_list,
        category_form=category_form,
        item_form=item_form
    )

@blueprint.route("/menu-edit/<name_hookah>/add-category", methods=['POST'])
@manager_required
def add_category(name_hookah):
    category_form = CategoryForm(request.form)
    if category_form.validate_on_submit:
        user = current_user._get_current_object()
        current_hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        new_category = Category(
            category_name = category_form.category_name.data,
            category_description = category_form.category_description.data,
            hookah_id = current_hookah.id,
            user_id = user.id
        )
        db.session.add(new_category)
        try:
            db.seesion.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили категорию {category_form.category_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Вы попытались создать категорию {category_form.category_name.data}, \
    которая уже существует, выберете другое название')
    return redirect(url_for('menu.menu-edit'))

@blueprint.route("/menu-edit/<name_hookah>/delete-category", methods=['GET', 'POST'])
@manager_required
def delete_category(name_hookah, category_name):
    category_delete_form = CategoryDeleteForm(request.form)
    if request.method == 'POST' and category_delete_form.validate_on_submit():
        hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        category = Category.query.filter_by(Category.hookah_id == hookah.id, category_name=category_name).first()
        db.session.delete(category)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы удалили категорию {category_delete_form.category_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Такой категории {category_delete_form.category_name.data} не существует')
    return render_template(
        'menu/delete-item.html',
        category=category,
        category_name=category_name,
        name_hookah=name_hookah,
    )


@blueprint.route("/menu-edit/<name_hookah>/add-item", methods=['POST'])
@manager_required
def add_item(name_hookah, category_name):
    item_form = ItemForm(request.form)
    if item_form.validate_on_submit:
        user = current_user._get_current_object()
        current_hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        current_category = Category.query.filter_by(category_name=category_name).first()
        new_item = Item(
            item_name = item_form.item_name.data,
            item_description = item_form.item_description.data,
            price = item_form.price.data,
            availability = item_form.availability.data,
            category_id = current_category.id,
            hookah_id = current_hookah.id,
            user_id = user.id
        )
        db.session.add(new_item)
        try:
            db.seesion.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы успешно добавили позицию {item_form.item_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Вы попытались создать позицию {item_form.item_name.data}, \
    которая уже существует, выберете другое название')
    return redirect(url_for('menu.menu-edit'))

@blueprint.route("/menu-edit/<name_hookah>", methods=['GET', 'POST'])
@manager_required
def delete_item(name_hookah, category_name, item_name):
    item_delete_form = ItemDeleteForm(request.form)
    if request.method == 'POST' and item_delete_form.validate_on_submit():
        hookah = Hookah.query.filter_by(name_hookah=name_hookah).first()
        current_category = Category.query.filter_by(category_name=category_name).first()
        item = Item.query.filter(Item.category_id == current_category.id, Item.hookah_id == hookah.id, item_name=item_name).first()
        db.session.delete(item)
        try:
            db.session.commit()
        except DBSaveException as e:
            print(e)
            db.session.rollback()
            raise DataBaseSaveError(e)
        flash(f'Вы удалили позицию {item_delete_form.item_name.data}')
        return redirect(url_for('menu.menu-edit'))
    flash(f'Такой позиции {item_delete_form.item_name.data} не существует')
    return render_template(
        'menu/delete-item.html',
        category_name=category_name,
        item=item,
        item_name=item_name,
        item_delete_form=item_delete_form,
        name_hookah=name_hookah
    )