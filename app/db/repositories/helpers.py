import sqlalchemy as sa

from app.db.engine import Meta


UserToGroups = sa.Table(
	"user_to_groups",
	Meta,
	sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
	sa.Column("group_id", sa.ForeignKey("groups.id"), primary_key=True),
)

ListsToProducts = sa.Table(
	"lists_to_products",
	Meta,
	sa.Column("product_list_id", sa.ForeignKey("product_lists.id"), primary_key=True),
	sa.Column("product_id", sa.ForeignKey("products.id"), primary_key=True),
)


PermissionsToGroups = sa.Table(
	"permissions_to_groups",
	Meta,
	sa.Column("group_id", sa.ForeignKey("groups.id"), primary_key=True),
	sa.Column("permission_id", sa.ForeignKey("permissions.id"), primary_key=True),
)
