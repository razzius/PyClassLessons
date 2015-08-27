#done when learning ajax stuff

@app.route('/not_ok', methods=["GET", "POST"])
def upvote():
    voted = request.form.items()
    print 'voted', voted
    vote = list(request.form.to_dict())
    print vote
    try:
        vote_id = int(vote.pop())
    except:
        vote_id = 0
    #query db by vote_id
    print 'vote_id', vote_id
    post_by_id = Post.query.filter_by(id=vote_id).first()
    print post_by_id
    #add 1 to points count
    post_by_id.points += 1
    # save to db
    db.session.commit()


    # print dir(request.form)
    print "vote_id", vote_id, "this was vote_id"
    print "vote", vote_id, "this was vote"
    print "request.args", request.args 
    dat = request.args.get('z', 1, type=int)
    dat2 = request.args.get('data', 1, type=int)
    dat3 = request.args.get('upvote_id', 1, type=int)
    print dat, dat2, dat3, "dats"
    print "request.form", request.form
    return json.dumps({'status':'OK', 'vote id':vote_id, 'dat':dat,'dat2':dat2, 'dat3':dat3})


@app.route('/_add_numbers', methods=["GET", "POST"])
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print a, b
    c = request.args.get('c', 0, type=int)
    print 'c', c
    print 'request.args', request.args 
    print jsonify(result = a+b)
    print jsonify({'value of c': c})
    return jsonify(result = a+b)

@app.route('/_more_add_numbers', methods=["GET", "POST"])
def more_add_numbers():
    print 'request.args', request.args
    e_num = request.args.get('e', type=int)
    print e_num
    return jsonify({e_num: e_num})