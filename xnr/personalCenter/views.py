#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('personalCenter', __name__, url_prefix='/personalCenter')

@mod.route('/individual/')
def personal_center():
    return render_template('personalCenter/personal_center.html')

