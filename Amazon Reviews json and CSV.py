from lxml import html
import requests,json,csv

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

headers = {'User-Agent': user_agent}
xpath_reviews = '//div[@data-hook="review"]'
xpath_rating  = './/i[@data-hook="review-star-rating"]//text()'
xpath_title   = './/a[@data-hook="review-title"]//text()'
xpath_author  = './/a[@data-hook="review-author"]//text()'
xpath_date    = './/span[@data-hook="review-date"]//text()'
xpath_body    = './/span[@data-hook="review-body"]//text()'
xpath_comment_count = './/span[@data-hook="review-comment"]//text()'

AsinList = ['B075SDL9CH','B077Y8JPDQ']
for asin in AsinList:
    pageNumber = 0
    extracted_data = []
    while (1):
        pageNumber +=1
        amazon_url = 'https://www.amazon.com/product-reviews/{}?pageNumber={}&sortBy=recent'.format(asin,pageNumber)
        page = requests.get(amazon_url, headers=headers)
        parser = html.fromstring(page.content)
        reviews = parser.xpath(xpath_reviews)
        if len(reviews)<1:
            break
        print("Downloading and processing page: ", amazon_url)
        for review in reviews:
            rating  = review.xpath(xpath_rating)
            rating  =' '.join(' '.join(rating).split())
            title   = review.xpath(xpath_title)
            title = ' '.join(' '.join(title).split())
            author  = review.xpath(xpath_author)
            author = ' '.join(' '.join(author).split())
            date    = review.xpath(xpath_date)
            date = ' '.join(' '.join(date).split())
            body    = review.xpath(xpath_body)
            body = ' '.join(' '.join(body).split())
            commcount = review.xpath(xpath_comment_count)
            commcount = ' '.join(' '.join(commcount).split())
            review_dict = {
                'review_comment_count': commcount,
                'review_text':body,
                'review_posted_date': date,
                'review_header':title,
                'review_rating':rating,
                'review_author':author,
                }
            extracted_data.append(review_dict)
            print(review_dict)

    f = open('{}.json'.format(asin), 'w')
    json.dump(extracted_data, f, indent=4)
    csvfile = '{}.csv'.format(asin)
    csvwriter = csv.writer(open(csvfile, 'w', newline='', encoding='utf-8'))
    count = 0
    for emp in extracted_data:
        if count == 0:
            try:
                header = emp.keys()
            except:
                header = emp
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(emp.values())



