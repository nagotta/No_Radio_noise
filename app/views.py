'''
ルート（エンドポイント）を定義します。
各エンドポイントで何を実行し、どのテンプレートをレンダリングするかを定義します。
'''
from ep1_app import app
from flask import render_template, jsonify, redirect, url_for, request
from urllib.parse import urlparse, parse_qs, urlunparse
from .scraper import StandFmScraper, YouTubeScraper, SpotifyScraper, TverScraper, RadiotalkScraper, RadikoScraper
from .models import Radio, Corner
from . import db
import re
from .mail import mail_template

def parse_url(url):
    youtube_regex = r"https://www\.youtube\.com/([^/]+)/videos"
    standfm_regex = r"https://stand\.fm/channels/([^/]+)"
    spotify_regex = r"https://open\.spotify\.com/show/([^/]+)"
    tver_regex =  r"https://tver\.jp/series/([^/]+)"
    radiotalk_regex =  r"https://radiotalk\.jp/program/([^/]+)"
    radiko_regex =  r"https://radiko\.jp/persons/([^/]+)"

    
    if re.match(youtube_regex, url):
        channel_type = "youtube"
        channel_id = re.match(youtube_regex, url).group(1)
    elif re.match(standfm_regex, url):
        channel_type = "standfm"
        channel_id = re.match(standfm_regex, url).group(1)
    elif re.match(spotify_regex, url):
        channel_type = "spotify"
        channel_id = re.match(spotify_regex, url).group(1)
    elif re.match(tver_regex, url):
        channel_type = "tver"
        channel_id = re.match(tver_regex, url).group(1)
    elif re.match(radiotalk_regex, url):
        channel_type = "radiotalk"
        channel_id = re.match(radiotalk_regex, url).group(1)
    elif re.match(radiko_regex, url):
        channel_type = "radiko"
        channel_id = re.match(radiko_regex, url).group(1)
    else:
        channel_type = "unknown"
        channel_id = ""

    return channel_type, channel_id


# rootURLにアクセス時
@app.route('/')
def index():
    radios = Radio.query.all()
    if len(radios) == 0:
        return redirect(url_for('register_radio'))
    else:
        urls = {
            "standfm": [],
            "youtube": [],
            "spotify": [],
            "tver": [],
            "radiotalk": [],
            "radiko": []
        }

        for radio in radios:
            channel_type = radio.channel_type
            channel_id = radio.channel_id

            if channel_type == "standfm":
                scraper = StandFmScraper(channel_id, 7, '.css-175oi2r a', 'https://stand.fm/episodes/')
            elif channel_type == "youtube":
                scraper = YouTubeScraper(channel_id, 7, 'a#thumbnail', 'https://www.youtube.com/watch?v=')
            elif channel_type == "spotify":
                scraper = SpotifyScraper(channel_id, 7, 'div.HLixBI5DbVZNC6lrUbAB a', 'https://open.spotify.com/episode/')
            elif channel_type == "tver":
                scraper = TverScraper(channel_id, 7, 'div.episode-pattern-c_container__7UBI_.episode-pattern-c_listContainer__4o6TL a', 'https://tver.jp/episodes/')
            elif channel_type == "radiotalk":
                scraper = RadiotalkScraper(channel_id, 7, 'div.program-action a', 'https://radiotalk.jp/talk/') 
            elif channel_type == "radiko":
                scraper = RadikoScraper(channel_id, 7, 'ul.styles__ProgramsStyle-sc-1lc98y3-0.tBmGT-programlist-items > li.styles__ProgramsStyle-sc-1lc98y3-0.tBmGT-programlist-item > a', 'https://radiko.jp/#!/ts/')
            else:
                continue

            url = scraper.get_latest_episode()
            scraper.quit()
            if channel_type in ["standfm", "spotify"]:
                parsed_url = urlparse(url)
                embed_url = urlunparse(parsed_url._replace(path='/embed' + parsed_url.path))
            elif channel_type == "youtube":
                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)
                embed_url = urlunparse(parsed_url._replace(path='/embed/' + params['v'][0], query=None))
            elif channel_type == "radiotalk":
                parsed_url = urlparse(url)
                new_path = parsed_url.path.replace('/talk/', '/embed/')
                embed_url = urlunparse(parsed_url._replace(path=new_path)) + "?color=navy"
            elif channel_type == "radiko":
                parsed_url = urlparse(url)
                station_id, datetime_string = parsed_url.fragment.split("/")[2:]
                embed_url = f"https://radiko.jp/embed/events?sid={station_id}&t={datetime_string}&type=default"
            else:
                embed_url = url
            urls[channel_type].append(embed_url)
            print(embed_url)

        return render_template('index.html', urls=urls)


@app.route('/register_radio', methods=['GET', 'POST'])
def register_radio():
    if request.method == 'GET':
        return render_template('register_radio.html')
    if request.method == 'POST':
        form_name = request.form.get('radioName')
        form_url = request.form.get('channelUrl')
        form_email = request.form.get('email')
        form_corner = request.form.get('cornerName')

        channel_type, channel_id = parse_url(form_url) 
        if channel_type == "unknown":  
            return jsonify({"error": "Invalid URL. The URL must follow one of the following patterns: https://stand.fm/channels/{any_value}, https://www.youtube.com/{any_value}/videos, https://open.spotify.com/show/{any_value}, https://tver.jp/series/{any_value}, https://radiotalk.jp/program/{any_value}"}), 400
        
        new_radio = Radio(
            name=form_name, 
            channel_type=channel_type,
            channel_id=channel_id,
            email=form_email
        )
        db.session.add(new_radio)
        db.session.flush()  # データベースに一時的に保存し、ID を取得する

        new_corner = Corner(
            radio_id=new_radio.id,
            corner_name=form_corner
        )
        db.session.add(new_corner)
                
        db.session.commit()  # 最終的にデータベースに保存する

        return redirect(url_for('index'))

@app.route('/check_db')
def employee_list():
    radios = Radio.query.all()
    return render_template('check_db.html', radios=radios)

@app.route('/register_corner', methods=['GET', 'POST'])
def register_corner():
    if request.method == 'GET':
        radios = Radio.query.all()
        radio_names = [radio.name for radio in radios]
        return render_template('register_corner.html', radio_names=radio_names)
    if request.method == 'POST':
        form_name = request.form.get('radioName')
        form_corner = request.form.get('cornerName')
        radio = Radio.query.filter_by(name=form_name).first()
        radio_id = radio.id if radio else None
        new_corner = Corner(
            radio_id=radio_id,
            corner_name=form_corner
        )
        db.session.add(new_corner)
        
        db.session.commit()
        return redirect(url_for('index'))
    
@app.route('/delete_radio', methods=['GET', 'POST'])
def delete_radio():
    if request.method == 'GET':
        radios = Radio.query.all()
        radio_names = [radio.name for radio in radios]
        return render_template('delete_radio.html', radio_names=radio_names)
    else:
        radio_name = request.json.get('radioName')
        radio = Radio.query.filter_by(name=radio_name).first()
        if radio:
            db.session.delete(radio)
            db.session.commit()
            return jsonify(success=True)  
        return jsonify(error="Radio not found"), 400

@app.route('/delete_corner', methods=['GET', 'POST'])
def delete_corner():
    if request.method == 'GET':
        radios = Radio.query.all()
        radio_names = [radio.name for radio in radios]
        first_radio = radios[0]
        corners = Corner.query.filter_by(radio_id=first_radio.id).all()
        corner_names = [corner.corner_name for corner in corners]
        return render_template('delete_corner.html', radio_names=radio_names, corner_names=corner_names)
    else:
        radio_name = request.json.get('radioName')
        corner_name = request.json.get('cornerName')
        radio = Radio.query.filter_by(name=radio_name).first()
        if radio:
            corner = Corner.query.filter_by(radio_id=radio.id, corner_name=corner_name).first()
            if corner:
                db.session.delete(corner)
                db.session.commit()
                return jsonify(success=True)  
            return jsonify({"error": "Corner not found"}), 400 
        return jsonify({"error": "Radio not found"}), 400


@app.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'GET':        
        radios = Radio.query.all()
        radio_names = [radio.name for radio in radios]
        first_radio = radios[0]
        corners = Corner.query.filter_by(radio_id=first_radio.id).all()
        corner_names = [corner.corner_name for corner in corners]
        return render_template('mail.html', radio_names=radio_names, corner_names=corner_names)
    if request.method == 'POST':
        radio_name = request.form.get('radioName')
        radio = Radio.query.filter_by(name=radio_name).first()
        if radio:
            to = radio.email
            subject = request.form.get('cornerName')
            body = request.form.get('content')
            mail = mail_template(to, subject, body)
            mail.send_email()
            return jsonify(success=True)
        else:
            return jsonify({"error": "Radio not found"}), 400  
    return jsonify({"error": "can't send mail"}), 400


@app.route('/get_corners/<radio_name>')
def get_corners(radio_name):
    radio = Radio.query.filter_by(name=radio_name).first()
    if radio:
        corners = Corner.query.filter_by(radio_id=radio.id).all()
        return jsonify([corner.corner_name for corner in corners])
    else:
        return jsonify([])
