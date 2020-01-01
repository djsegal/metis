import collections

SubwayLine = collections.namedtuple(
    'SubwayLine', 'name color letters'
)

subway_lines = [
    SubwayLine(name='Blue', color="#0039A6", letters="a c e".upper().split()),
    SubwayLine(name='Orange', color="#FF6319", letters="b d f m".upper().split()),
    SubwayLine(name='G', color="#6CBE45", letters="g".upper().split()),
    SubwayLine(name='Brown', color="#996633", letters="j z".upper().split()),
    SubwayLine(name='L', color="#A7A9AC", letters="l".upper().split()),
    SubwayLine(name='Yellow', color="#FCCC0A", letters="n q r w".upper().split()),
    SubwayLine(name='S', color="#808183", letters="s".upper().split()),
    SubwayLine(name='Red', color="#EE352E", letters="1 2 3".upper().split()),
    SubwayLine(name='Green', color="#00933C", letters="4 5 6".upper().split()),
    SubwayLine(name='7', color="#B933AD", letters="7".upper().split())
]

def group_subway_lines(cur_lines):
    line_set = set()

    for cur_line in cur_lines:
        tmp_name = None
        for subway_line in subway_lines:
            if cur_line not in subway_line.letters : continue

            tmp_name = subway_line.name
            break

        assert tmp_name != None
        line_set.add(tmp_name)

    assert len(line_set) > 0
    return list(line_set)
