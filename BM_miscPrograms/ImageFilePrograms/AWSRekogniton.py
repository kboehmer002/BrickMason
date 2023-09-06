import boto3

#base example - will modify later, source: https://www.youtube.com/watch?v=Q-l9KjDNUKc&list=PLlvAxgO7JdIVFhKszt8Oxi5opB7N-byws&index=3
#This example uses images stored in an S3 bucket, can also use Rekognition on local images

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("    Top: " + str(instance['BoundingBox']['Top']))
            print ("    Left: " + str(instance['BoundingBox']['Left']))
            print ("    Width: " +  str(instance['BoundingBox']['Width']))
            print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
    return len(response['Labels'])


def main():
    photo='bronxZoo1.jpg'
    bucket='rekognition-playground283'
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
