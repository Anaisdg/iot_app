# write_data.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db

# @auth.route('/login', methods=['POST'])