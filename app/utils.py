def match_meta(form, max_form_len):
    n_fields = len(form) - max_form_len
    meta = dict()
    for i in range(n_fields):
        if 'name_{0}'.format(i) in form:
            if (form['name_{0}'.format(i)].strip() != '')and(form['val_{0}'.format(i)].strip() != ''):
                meta[form['name_{0}'.format(i)]] = form['val_{0}'.format(i)]
    return meta
