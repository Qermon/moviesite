from django.test import TestCase

from film.forms import RatingForm


class RatingFormTest(TestCase):

    def test_form_fields_classes_and_attributes(self):
        form = RatingForm()

        self.assertEqual(form.fields['review'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['review'].widget.attrs['placeholder'], 'Write your review')
        self.assertEqual(form.fields['review'].widget.attrs['rows'], 4)
        self.assertEqual(form.fields['user_rate'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['user_rate'].widget.attrs['min'], 1)
        self.assertEqual(form.fields['user_rate'].widget.attrs['max'], 10)

    def test_user_rate_initial_value(self):
        form = RatingForm()
        self.assertEqual(form.fields['user_rate'].initial, 0)

    def test_form_valid_data(self):
        form_data = {
            'review': 'Good!',
            'user_rate': 8
        }
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_rate(self):
        form_data = {
            'review': 'Bad!',
            'user_rate': -1
        }
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_user_rate_high(self):
        form_data = {
            'review': 'Good!',
            'user_rate': 11
        }
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_empty_review(self):
        form_data = {
            'review': '',
            'user_rate': 5
        }
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid(), "The field review cant be empty")

    def test_form_invalid_missing_fields(self):
        form_data = {
            'user_rate': 7
        }
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_missing_rate(self):
        form_data = {
            'review': 'Good!',
        }
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_long_review(self):
        form_data = {
            'review': '111111111111111111111111111111111111111111111111111111111111111111111111111111',
            'user_rate': 9
        }
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())


