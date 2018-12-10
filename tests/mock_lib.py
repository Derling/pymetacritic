def create_legacy_review_tag(classes, body):
	li_classes = ' '.join(classes)
	expanded_body = len(body) >= 400
	span_class = '' if not expanded_body else ' class="blurb blurb_expanded"'
	return f'<li class="{li_classes}"><span{span_class}>{body}</span></li>'


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


def create_legacy_review_elements(reviews, reviewers):
	review_elements = get_legacy_review_elements(reviews, reviewers)
	return f'''<ol class="reviews {reviewers}_reviews">{review_elements}</ol>'''

