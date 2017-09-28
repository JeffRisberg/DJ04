# django
from django.db.models import QuerySet, F


class BaseQuerySet(QuerySet):
    def order_by(self, *field_names):
        """
        Fixes `ORDER BY is ambiguous` error.
        This occurs on annotated fields that have a similar name to
        a related field.

        In our case, the annotated `converted_balance` on {Invoice,Bill}
        was causing an error when ordering whenever .select_related()
        was called on 'vendor' or 'customer' because those objects also
        have a `converted_balance` field.
        """
        updated_field_names = []
        for field_name in field_names:
            if isinstance(field_name, basestring) and field_name != '?':
                is_desc = field_name.startswith('-')

                # Remove `-` if field_name has it
                if is_desc:
                    field_name = field_name[1:]

                field_name = F(field_name).desc() if is_desc else F(field_name).asc()

            updated_field_names.append(field_name)

        return super(BaseQuerySet, self).order_by(*updated_field_names)
