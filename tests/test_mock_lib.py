from .mock_lib import (
	create_legacy_review_tag,
	get_legacy_review_elements,
	create_legacy_review_elements,
	get_legacy_review_div
)


def test_create_legacy_review_tag_returns_correct_string_tag():
	return_value = create_legacy_review_tag(['fake_class'], 'body_of_element')
	assert return_value == '<li class="fake_class">' \
						   '<div class="review_body">' \
						   '<span>body_of_element</span>' \
						   '</div>'\
						   '</li>'


def test_create_legacy_review_tag_adds_class_to_span_with_large_review_body():
	review_body = 'awesome review' * 40
	return_value = create_legacy_review_tag(['fake_class'], review_body)
	assert return_value == '<li class="fake_class">' \
						   '<div class="review_body">' \
						   f'<span class="blurb blurb_expanded">{review_body}</span>' \
						   '</div>' \
						   '</li>'


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
	assert return_value == '<li class="review critic_review first_review">' \
						   '<div class="review_body">' \
						   '<span>review # 1</span>' \
						   '</div>' \
						   '</li>' \
					 	   '<li class="review critic_review last_review">' \
					 	   '<div class="review_body">'\
					 	   '<span>review # 2</span>' \
					 	   '</div>' \
					 	   '</li>'


def test_get_legacy_review_elements_returns_correct_string_for_two_reviews_for_users():
	return_value = get_legacy_review_elements(['review # 1', 'review # 2'], 'user')
	assert return_value == '<li class="review user_review first_review">' \
						   '<div class="review_body">' \
						   '<span>review # 1</span>' \
						   '</div>' \
						   '</li>' \
					 	   '<li class="review user_review last_review">' \
					 	   '<div class="review_body">' \
					 	   '<span>review # 2</span>' \
					 	   '</div>' \
					 	   '</li>'


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_critics():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'critic')
	assert  return_value == '<li class="review critic_review first_review">' \
							'<div class="review_body">' \
							'<span>first</span>' \
							'</div>' \
							'</li>' \
					 		'<li class="review critic_review">' \
					 		'<div class="review_body">' \
					 		'<span>second</span>' \
					 		'</div>' \
					 		'</li>' \
						 	'<li class="review critic_review last_review">' \
						 	'<div class="review_body">' \
						 	'<span>third</span>' \
						 	'</div>' \
						 	'</li>'


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_users():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'user')
	assert return_value == '<li class="review user_review first_review">' \
						   '<div class="review_body">' \
						   '<span>first</span>' \
						   '</div>' \
						   '</li>' \
					 	   '<li class="review user_review">' \
					 	   '<div class="review_body">' \
					 	   '<span>second</span>' \
					 	   '</div>' \
					 	   '</li>' \
					 	   '<li class="review user_review last_review">' \
					 	   '<div class="review_body">' \
					 	   '<span>third</span>' \
					 	   '</div>' \
					 	   '</li>'


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
					 	   '<div class="review_body">' \
					 	   '<span>review</span>' \
					 	   '</div>' \
					 	   '</li>' \
					       '</ol>'


def test_create_legacy_review_elements_returns_correct_string_for_one_review_for_critics():
	return_value = create_legacy_review_elements(['review'], 'critic')
	assert return_value == '<ol class="reviews critic_reviews">' \
					 	   '<li class="review critic_review first_review last_review">' \
					 	   '<div class="review_body">' \
					 	   '<span>review</span>' \
					 	   '</div>' \
						   '</li>' \
						   '</ol>'


def test_get_legacy_review_div_returns_correct_div_without_expanded_body():
	return_value = get_legacy_review_div('review', False, 'class')
	assert return_value == '<div class="class">' \
						   '<span>review</span>' \
						   '</div>'


def test_get_legacy_review_div_returns_correct_div_with_expanded_body():
	return_value = get_legacy_review_div('review', True, 'class')
	assert return_value == '<div class="class">' \
						   '<span class="blurb blurb_expanded">review</span>' \
						   '</div>'
