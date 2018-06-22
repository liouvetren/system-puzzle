from wtforms import StringField,Form,IntegerField
from wtforms.validators import DataRequired

class ItemForm(Form):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])

