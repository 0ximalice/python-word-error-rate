"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""

import numpy


def wer(r, h):

    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """

    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    result = float(d[len(r)][len(h)]) / len(r) * 100
    print('WER %.4f %%' % result)

    x = len(r)
    y = len(h)

    html = '<html><body><head><meta charset="utf-8"></head>' \
           '<style>.g{background-color:#0080004d}.r{background-color:#ff00004d}.y{background-color:#ffa50099}</style>'

    while True:
        if x == 0 or y == 0:
            break

        if r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            html = '%s ' % h[y] + html
        elif d[x][y] == d[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            html = '<span class="y">%s(%s)</span> ' % (h[y], r[x]) + html
        elif d[x][y] == d[x - 1][y] + 1:        # deletion
            x = x - 1
            html = '<span class="r">%s</span> ' % r[x] + html
        elif d[x][y] == d[x][y - 1] + 1:        # insertion
            y = y - 1
            html = '<span class="g">%s</span> ' % h[y] + html
        else:
            print('\nWe got an error.')
            break

    html = html + '</body></html>'

    with open('diff.html', 'w', encoding='utf8') as f:
        f.write(html)
        f.close()
