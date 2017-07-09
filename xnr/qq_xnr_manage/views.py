#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from xnr.parameter import MAX_VALUE
from utils import show_qq_xnr, create_qq_xnr, delete_qq_xnr, change_qq_xnr,\
                  search_qq_xnr


mod = Blueprint('qq_xnr_manage', __name__, url_prefix='/qq_xnr_manage')


@mod.route('/add_qq_xnr/')
def ajax_add_qq_xnr():
    qq_number = request.args.get('qq_number','')
    qq_groups = request.args.get('qq_groups','')
    nickname = request.args.get('qq_nickname','')
    active_time = request.args.get('qq_active_time')
    xnr_info = [qq_number,qq_groups,nickname,active_time]
    result = create_qq_xnr(xnr_info)
    return json.dumps(result)

@mod.route('/delete_qq_xnr/')
def ajax_delete_qq_xnr():
    qq_number = request.args.get('qq_number','')
    results = delete_qq_xnr(qq_number)
    return json.dumps(results)

@mod.route('/show_qq_xnr/')
def ajax_show_qq_xnr():
    results = {}
    results = show_qq_xnr(MAX_VALUE)
    return json.dumps(results)

@mod.route('/change_qq_xnr/')
def ajax_change_qq_xnr():
    qq_number = request.args.get('qq_number','')
    qq_groups = request.args.get('qq_groups','')
    xnr_info = [qq_number,qq_groups]
    results = change_qq_xnr(xnr_info)
    return json.dumps(results)

@mod.route('/search_qq_xnr/')
def ajax_search_qq_xnr():
    qq_number = request.args.get('qq_number','')
    results = search_qq_xnr(qq_number)
    return json.dumps(results)