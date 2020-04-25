# main.py
import requests
import argparse
import json
import constants

def getClaimReviews(formattedKeywords):
    response = requests.get(
        url=constants.URL,
        params=dict(
            key=constants.API_KEY,
            languageCode=constants.LANGUAGECODE,
            query=formattedKeywords))
    return response.json()

def formatString(keywords):
    queryList = keywords.split()
    return '%20'.join(s for s in queryList)

def jsonEvaluation(jsonContent):
    falseHits = 0
    for claim in jsonContent['claims']:
        if "False" in claim['claimReview'][0]['textualRating']:
            falseHits += 1
    if falseHits > (len(jsonContent['claims'])//2):
        return True
    else:
        return False

def prettyPrint(jsonContent):
	print(json.dumps(jsonContent, indent=4, sort_keys=True))

def main():
    parser = argparse.ArgumentParser(description='Provides likelihood keywords are found in fake news')
    parser.add_argument('keywords', type=str, help='keywords to match')
    parser.add_argument('-p', action='store_true', help='Output claims in console')
    args = parser.parse_args()

    claimReviews = getClaimReviews(formatString(args.keywords))
    if args.p:
    	prettyPrint(claimReviews)
    if jsonEvaluation(claimReviews):
        print("Likely fake news")
    

if __name__ == "__main__":
    main()
