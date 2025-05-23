from flask import Blueprint, render_template, request, abort, flash
from peewee import fn
from app.models import User
from app.utils.load_service import load_users


user_registry_bp = Blueprint(
    name='user_pages',
    import_name=__name__,
    template_folder='templates'
)


class PaginationContext:
    def __init__(
        self,
        elements_per_page: int,
        total_elements: int,
        current_page: int
    ) -> None:
        self.total_pages = (
            (total_elements + elements_per_page - 1) // elements_per_page
        )
        if current_page < 1:
            self.current_page = 1
        elif current_page > self.total_pages and self.total_pages != 0:
            self.current_page = self.total_pages
        else:
            self.current_page = current_page


@user_registry_bp.route('/', methods=['GET', 'POST'])
def list_users():
    USERS_PER_PAGE = 10

    if request.method == 'POST':
        users_amount = request.form.get('users_amount', type=int)
        if not users_amount or users_amount < 0 or users_amount > 5000:
            flash('Amount of users should be in range from 0 to 5000', 'error')
        else:
            load_users(users_amount)


    total_users = User.select().count()

    pagination_context = PaginationContext(
        elements_per_page=USERS_PER_PAGE,
        total_elements=total_users,
        current_page=request.args.get('page', 1, type=int)
    )

    users = User.select().paginate(
        pagination_context.current_page,
        USERS_PER_PAGE
    )

    return render_template(
        'index.html',
        users=users,
        total_users=total_users,
        pagination=pagination_context,
    )


@user_registry_bp.route('/<int:user_id>')
def user_details(user_id: int):
    if user_id < 0:
        abort(400)

    user = User.select().where(User.id == user_id).get_or_none()
    if user is None:
        abort(404)

    return render_template(
        'user_details.html',
        user=user,
    )


@user_registry_bp.route('/random')
def random_user_details():
    user = User.select().order_by(fn.Random()).limit(1).first()
    if not user:
        return "Looks like there is no users to show", 200

    return render_template(
        'user_details.html',
        user=user,
    )
