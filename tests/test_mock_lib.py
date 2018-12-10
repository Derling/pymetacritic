from .mock_lib import (
	create_legacy_review_tag,
	get_legacy_review_elements,
	create_legacy_review_elements
)


def test_create_legacy_review_tag_returns_correct_string_tag():
	return_value = create_legacy_review_tag(['fake_class'], 'body_of_element')
	expected_return_value = '<li class="fake_class"><span>body_of_element</span></li>'
	assert return_value == expected_return_value


def test_create_legacy_review_tag_adds_class_to_span_with_large_review_body():
	review_body = 'awesome review' * 40
	return_value = create_legacy_review_tag(['fake_class'], review_body)
	expected_return_value = f'<li class="fake_class"><span class="blurb blurb_expanded">{review_body}</span></li>'
	assert return_value == expected_return_value


def test_get_legacy_review_elements_contains_correct_review_body_in_element():
	review_body = 'review 1'
	return_value = get_legacy_review_elements([review_body], 'critic')
	assert review_body in return_value


def test_get_legacy_review_elements_returns_one_element_with_one_review_with_correct_class_for_critics():
	return_value = get_legacy_review_elements(['review # 1'], 'critic')
	expected_class = 'class="review critic_review first_review last_review"'
	assert expected_class in return_value


def test_get_legacy_review_elements_returns_one_element_with_one_review_with_correct_class_for_users():
	return_value = get_legacy_review_elements(['review # 1'], 'user')
	expected_class = 'class="review user_review first_review last_review"'
	assert expected_class in return_value


def test_get_legacy_review_elements_returns_correct_string_for_two_reviews_for_critics():
	return_value = get_legacy_review_elements(['review # 1', 'review # 2'], 'critic')
	expected_value = '<li class="review critic_review first_review"><span>review # 1</span></li>' \
					 '<li class="review critic_review last_review"><span>review # 2</span></li>'
	assert expected_value == return_value


def test_get_legacy_review_elements_returns_correct_string_for_two_reviews_for_users():
	return_value = get_legacy_review_elements(['review # 1', 'review # 2'], 'user')
	expected_value = '<li class="review user_review first_review"><span>review # 1</span></li>' \
					 '<li class="review user_review last_review"><span>review # 2</span></li>'
	assert expected_value == return_value


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_critics():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'critic')
	expected_value = '<li class="review critic_review first_review"><span>first</span></li>' \
					 '<li class="review critic_review"><span>second</span></li>' \
					 '<li class="review critic_review last_review"><span>third</span></li>'
	assert expected_value == return_value


def test_get_legacy_review_elements_returns_correct_string_for_more_than_two_reviews_for_users():
	return_value = get_legacy_review_elements(['first', 'second', 'third'], 'user')
	expected_value = '<li class="review user_review first_review"><span>first</span></li>' \
					 '<li class="review user_review"><span>second</span></li>' \
					 '<li class="review user_review last_review"><span>third</span></li>'
	assert expected_value == return_value


def test_get_legacy_review_element_has_correct_number_of_elements_for_multiple_reviews_for_critics():
	reviews = ['first', 'second', 'third', 'fourth', 'fifth']
	return_value = get_legacy_review_elements(reviews, 'critic')
	expected_number_of_elements = [1, 3, 1]
	assert [
		return_value.count('class="review critic_review first_review"'),
		return_value.count('class="review critic_review"'),
		return_value.count('class="review critic_review last_review"')
	] == expected_number_of_elements


def test_get_legacy_review_element_has_correct_number_of_elements_for_multiple_reviews_for_users():
	reviews = ['first', 'second', 'third', 'fourth', 'fifth']
	return_value = get_legacy_review_elements(reviews, 'user')
	expected_number_of_elements = [1, 3, 1]
	assert [
		return_value.count('class="review user_review first_review"'),
		return_value.count('class="review user_review"'),
		return_value.count('class="review user_review last_review"')
	] == expected_number_of_elements


def test_create_legacy_review_elements_returns_correct_string_for_one_review_for_users():
	return_value = create_legacy_review_elements(['review'], 'user')
	expected_value = '<ol class="reviews user_reviews">' \
					 '<li class="review user_review first_review last_review">' \
					 '<span>review</span>' \
					 '</li>' \
					 '</ol>'
	assert return_value == expected_value


def test_create_legacy_review_elements_returns_correct_string_for_one_review_for_critics():
	return_value = create_legacy_review_elements(['review'], 'critic')
	expected_value = '<ol class="reviews critic_reviews">' \
					 '<li class="review critic_review first_review last_review">' \
					 '<span>review</span>' \
					 '</li>' \
					 '</ol>'
	assert return_value == expected_value
