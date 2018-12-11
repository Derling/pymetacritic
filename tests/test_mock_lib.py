from .mock_lib import (
	create_legacy_review_tag,
	get_legacy_review_elements,
	create_legacy_review_elements
)


def test_create_legacy_review_tag_returns_correct_string_tag():
	return_value = create_legacy_review_tag(['fake_class'], 'body_of_element')
	assert return_value == '<li class="fake_class"><span>body_of_element</span></li>'


def test_create_legacy_review_tag_adds_class_to_span_with_large_review_body():
	review_body = 'awesome review' * 40
	return_value = create_legacy_review_tag(['fake_class'], review_body)
	assert return_value == f'<li class="fake_class"><span class="blurb blurb_expanded">{review_body}</span></li>'


def test_get_legacy_review_elements_contains_correct_review_body_in_element():
	review_body = 'review 1'
	return_value = get_legacy_review_elements([review_body], 'critic')
	assert review_body in return_value


def test_get_legacy_review_elements_returns_one_element_with_one_review_with_correct_class_for_critics():
	return_value = get_legacy_review_elements(['review # 1'], 'critic')
	assert 'class="review critic_review first_review last_review"' in return_value


def test_get_legacy_review_elements_returns_one_element_with_one_review_with_correct_class_for_users():
	return_value = get_legacy_review_elements(['review # 1'], 'user')
	assert 'class="review user_review first_review last_review"' in return_value


def test_get_legacy_review_elements_returns_correct_string_for_two_reviews_for_critics():
	return_value = get_legacy_review_elements(['review # 1', 'review # 2'], 'critic')
	assert return_value == '<li class="review critic_review first_review"><span>review # 1</span></li>' \
					 	   '<li class="review critic_review last_review"><span>review # 2</span></li>'


def test_get_legacy_review_elements_returns_correct_string_for_two_reviews_for_users():
	return_value = get_legacy_review_elements(['review # 1', 'review # 2'], 'user')
	assert return_value == '<li class="review user_review first_review"><span>review # 1</span></li>' \
					 	   '<li class="review user_review last_review"><span>review # 2</span></li>'


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_critics():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'critic')
	assert  return_value == '<li class="review critic_review first_review"><span>first</span></li>' \
					 		'<li class="review critic_review"><span>second</span></li>' \
						 	'<li class="review critic_review last_review"><span>third</span></li>'


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_users():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'user')
	assert return_value == '<li class="review user_review first_review"><span>first</span></li>' \
					 	   '<li class="review user_review"><span>second</span></li>' \
					 	   '<li class="review user_review last_review"><span>third</span></li>'


def test_get_legacy_review_element_has_correct_number_of_elements_for_multiple_reviews_for_critics():
	reviews = ['first', 'second', 'third', 'fourth', 'fifth']
	return_value = get_legacy_review_elements(reviews, 'critic')
	assert [
		return_value.count('class="review critic_review first_review"'),
		return_value.count('class="review critic_review"'),
		return_value.count('class="review critic_review last_review"')
	] == [1, 3, 1]


def test_get_legacy_review_element_has_correct_number_of_elements_for_multiple_reviews_for_users():
	reviews = ['first', 'second', 'third', 'fourth', 'fifth']
	return_value = get_legacy_review_elements(reviews, 'user')
	assert [
		return_value.count('class="review user_review first_review"'),
		return_value.count('class="review user_review"'),
		return_value.count('class="review user_review last_review"')
	] == [1, 3, 1]


def test_create_legacy_review_elements_returns_correct_string_for_one_review_for_users():
	return_value = create_legacy_review_elements(['review'], 'user')
	assert return_value == '<ol class="reviews user_reviews">' \
					 	   '<li class="review user_review first_review last_review">' \
					 	   '<span>review</span>' \
					 	   '</li>' \
					       '</ol>'


def test_create_legacy_review_elements_returns_correct_string_for_one_review_for_critics():
	return_value = create_legacy_review_elements(['review'], 'critic')
	assert return_value == '<ol class="reviews critic_reviews">' \
					 	   '<li class="review critic_review first_review last_review">' \
					 	   '<span>review</span>' \
						   '</li>' \
						   '</ol>'
