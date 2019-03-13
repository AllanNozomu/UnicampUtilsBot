# UnicampUtilsBot
A Telegram bot that I still do not know what It is going to do but...
The main idea is to do a serverless bot using AWS Lambda and some persistance using S3 or some database (RDS or DynamoDB). Also try to wrap things that I am discovering now like `pdftotext` things.

# Future features

## Under development

1. Alert the student which is the next class and where (one hour before) **UNDER DEVELOPMENT**
    1. Do this automatically, just send the pdf of the Relatorio de Matricula, parse it and save
    1. Or do this giving the DAC RA and password

## Planned features

1. Location finder: show where some room or institure is
1. Bandex advisor
    1. Show the week menu and also track the best menus (maybe Feijoada)
1. Maybe some *"how much money do I have feature"* in my RA card 

## Useful links that I (am) read(ind) to do this

1. This was the kickstarter [article](https://medium.freecodecamp.org/how-to-build-a-server-less-telegram-bot-227f842f4706)
1. Also interesting [article](https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg)
1. I am using [Flask](http://flask.pocoo.org/) and [requests](http://docs.python-requests.org/en/master/) to do things
1. I am using [Zappa](https://github.com/Miserlou/Zappa) to deploy to AWS Lambda. It is awesome
1. [Telegram bot API](https://core.telegram.org/bots/api) of course (This is what I am doing)
1. Used some code in this [repo](https://github.com/skylander86/lambda-text-extractor) to make `pdftotext` works properky

## Related cool stuff

1. [Serverless](https://serverless.com/)
1. [Chalice](https://github.com/aws/chalice)

This is a sample README that I will modify later. Just some ideas about a thing that I do not know yet.
