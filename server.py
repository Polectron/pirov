from bottle import route, run, request
import pygame
import RPi.GPIO as io

@route('/updateinputs')
def index():
    print(request.POST.get("type"))
    return 'updating inputs'

run(host='0.0.0.0', port=8081)