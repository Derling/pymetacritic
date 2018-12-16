# helpers


def get_modern_div_wrapper(div_class, child_element):
	return f'<div class="{div_class}">{child_element}</div>'


def get_modern_critic_review_div(review):
	return f'<div class="summary"><a class="no_hover">{review}</a></div>'


def get_modern_review_elements_for_critics(reviews, wrapper_class):
	review_elements = []

	for review in reviews:
		review_div = get_modern_critic_review_div(review)
		review_elements.append(get_modern_div_wrapper(wrapper_class, review_div))

	return ''.join(review_elements)


def get_modern_review_elements_for_users(reviews, wrapper_class):
	review_elements = []

	for review in reviews:
		expanded_body = len(review) >= 400
		review_div = get_legacy_review_div(review, expanded_body, 'summary')
		review_elements.append(get_modern_div_wrapper(wrapper_class, review_div))

	return ''.join(review_elements)


def get_legacy_review_div(review_body, expanded_body, div_class):
	span_class = '' if not expanded_body else ' class="blurb blurb_expanded"'
	return f'<div class="{div_class}"><span{span_class}>{review_body}</span></div>'


def create_legacy_review_tag(classes, body):
	li_classes = ' '.join(classes)
	expanded_body = len(body) >= 400
	review_div = get_legacy_review_div(body, expanded_body, 'review_body')
	return f'<li class="{li_classes}">{review_div}</li>'


def get_legacy_review_elements(reviews, reviewers):
	if len(reviews) == 1:
		review = reviews[0]
		classes = ['review', f'{reviewers}_review', 'first_review', 'last_review']
		review_tag = create_legacy_review_tag(classes, review)
		return review_tag

	first_review_tag = create_legacy_review_tag(['review', f'{reviewers}_review', 'first_review'], reviews[0])
	review_elements = [first_review_tag]

	for i in range(1, len(reviews) - 1):
		review_tag = create_legacy_review_tag(['review', f'{reviewers}_review'], reviews[i])
		review_elements.append(review_tag)

	last_review_tag = create_legacy_review_tag(['review', f'{reviewers}_review', 'last_review'], reviews[-1])
	review_elements.append(last_review_tag)

	return ''.join(review_elements)

# lib fucntions


def create_legacy_review_elements(reviews, reviewers):
	if not len(reviews):
		return ''
	review_elements = get_legacy_review_elements(reviews, reviewers)
	return f'<ol class="reviews {reviewers}_reviews">{review_elements}</ol>'


def create_modern_review_elements_for_critics(reviews):
	if not len(reviews):
		return ''
	review_elements = get_modern_review_elements_for_critics(reviews, 'review pad_top1 pad_btm1')
	return f'<div class="critic_reviews">{review_elements}</div>'


def create_modern_review_elements_for_users(reviews):
	if not len(reviews):
		return ''
	review_elements = get_modern_review_elements_for_users(reviews, 'review pad_top1')
	return f'<div class="user_reviews">{review_elements}</div>'
