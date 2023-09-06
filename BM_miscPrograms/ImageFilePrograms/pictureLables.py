import boto3

'''Given a single image file, returns a word list of objects detected in the image, using Rekognition'''

def labelImageObjects(image):
    # Create AWS Rekognition client
    client = boto3.client('rekognition')

    # Read image
    with open(image, 'rb') as image:
        image_bytes = image.read()

    # Use Rekognition to detect objects within the image (using bytes parameter to avoid using S3 buckets in this case)
    response = client.detect_labels(Image={'Bytes': image_bytes})

    # Only interested in labels - get the labels from the Rekognition analysis job
    labels = response['Labels']

    # Create a list of words from the label names
    words = [label['Name'] for label in labels]

    # Return the list of words
    return words

# ---------------------------------
'''picture = './BM_simplePrograms/ImageFilePrograms/critter.jpg'
tags = labelImageObjects(picture)
print(tags)'''

# -------------------------------------------------------------------------------------

'''Accept multiple images (a list of image files) and return list of a label list for each image'''

def batchLabelImageObjects(images):

    client = boto3.client('rekognition')
    # initialize return variable
    results = []

    # iterate through images
    for image in images:
        
        with open(image, 'rb') as image:
            image_bytes = image.read()
        
        response = client.detect_labels(Image={'Bytes': image_bytes})
        
        labels = [label['Name'] for label in response['Labels']]
        
        results.append(labels)

    return results

# ----------------------------------------------------------------


image_files = ['./BM_simplePrograms/ImageFilePrograms/clarkChristmas.jpg', './BM_simplePrograms/ImageFilePrograms/clarkOutside.jpg',
               './BM_simplePrograms/ImageFilePrograms/violet.jpg', './BM_simplePrograms/ImageFilePrograms/critter.jpg']

# print picture title followed by tags - each pic separated with a line


def formattedPrint(list):
    for listItem in list:
        print("picture")
        print(listItem)
        print("\n")


'''tags_list = labelImageObjects('./BM_simplePrograms/ImageFilePrograms/clarkChristmas.jpg')
print(tags_list)'''

batchTags = batchLabelImageObjects(image_files)
formattedPrint(batchTags)
