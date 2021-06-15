#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import json
import requests
import json, re
from dateutil import parser as dateparser
from time import sleep

def multiple_review(asin):
    pageNumber = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    xpath_reviews = '//div[@data-hook="review"]'
    xpath_rating = './/i[@data-hook="review-star-rating"]//text()'
    xpath_title = './/a[@data-hook="review-title"]//text()'
    xpath_author = './/a[@data-hook="review-author"]//text()'
    xpath_date = './/span[@data-hook="review-date"]//text()'
    xpath_body = './/span[@data-hook="review-body"]//text()'
    xpath_comment_count = './/span[@data-hook="review-comment"]//text()'
    reviews_list = []
    while (1):
        pageNumber +=1
        review_url = 'https://www.amazon.com/product-reviews/{}?pageNumber={}&sortBy=recent'.format(asin,pageNumber)
        page = requests.get(review_url, headers=headers)
        parser = html.fromstring(page.content)
        reviews = parser.xpath(xpath_reviews)
        if len(reviews)<1:
            break
        print("\tGetting Reviews from: ", review_url)
        for review in reviews:
            rating  = review.xpath(xpath_rating)
            rating  =''.join(rating).replace('out of 5 stars', '')

            title   = review.xpath(xpath_title)
            title = ' '.join(' '.join(title).split())

            author  = review.xpath(xpath_author)
            author = ' '.join(' '.join(author).split())

            date    = review.xpath(xpath_date)
            try:
                date = dateparser.parse(''.join(date)).strftime('%d %b %Y')
            except:
                date = None

            body    = review.xpath(xpath_body)
            body = ' '.join(' '.join(body).split())

            review_comments = review.xpath(xpath_comment_count)
            review_comments = ''.join(review_comments)
            review_comments = re.sub('[A-Za-z]', '', review_comments).strip()

            review_dict = {
                'review_comment_count': review_comments,
                'review_text':body,
                'review_posted_date': date,
                'review_header':title,
                'review_rating':rating,
                'review_author':author,
                }
            reviews_list.append(review_dict)
    return (reviews_list)

def ParseReviews(asin):
    amazon_url = 'http://www.amazon.in/dp/' + asin

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(amazon_url, headers=headers, verify=False)
    page_response = page.text

    parser = html.fromstring(page_response)
    XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
    XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
    XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

    XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
    XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
    XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

    raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    product_price = ''.join(raw_product_price).replace(',', '')

    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    product_name = ''.join(raw_product_name).strip()
    total_ratings = parser.xpath(XPATH_AGGREGATE_RATING)
    reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
    if not reviews:
        reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
    ratings_dict = {}

    if not reviews:
        raise ValueError('unable to find reviews in page')
    else:
        reviews_list = multiple_review(asin)  # NEW Function added
    # grabing the rating  section in product page
    for ratings in total_ratings:
        extracted_rating = ratings.xpath('./td//a//text()')
        if extracted_rating:
            rating_key = extracted_rating[0]
            raw_raing_value = extracted_rating[1]
            rating_value = raw_raing_value
            if rating_key:
                ratings_dict.update({rating_key: rating_value})

    # Parsing individual reviews



    data = {
        'ratings': ratings_dict,
        'reviews': reviews_list,
        'url': amazon_url,
        'price': product_price,
        'name': product_name
    }
    return data


# 	except ValueError:
# 		print("Retrying to get the correct response")

# return {"error":"failed to process the page","asin":asin}

def ReadAsin():
    # Add your own ASINs here
    AsinList = ['B09WRMNJ9G']
    extracted_data = []
    for asin in AsinList:
        print("Downloading and processing page http://www.amazon.in/dp/" + asin)
        extracted_data.append(ParseReviews(asin))
        print("#######")
        print(extracted_data);
        sleep(5)
        f = open('{}.json'.format(asin), 'w')
        json.dump(extracted_data, f, indent=4)


if __name__ == '__main__':
    ReadAsin()



