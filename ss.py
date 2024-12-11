from decimal import Decimal

ok = """
0
121.440387,31.192979
1
121.441185,31.190913
2
121.441285,31.190963
3
121.441085,31.191013
4
121.441385,31.190863
5
121.440985,31.190813
6
121.439846,31.19364
7
121.439746,31.19354
8
121.439646,31.19359
9
121.439946,31.19374
10
121.440046,31.19369
11
121.441448,31.192138
12
121.441548,31.192188
13
121.441648,31.192238
14
121.441348,31.192038
15
121.441248,31.192088
16
121.44049,31.194069
17
121.44059,31.194169
18
121.44069,31.194119
19
121.44039,31.193969
20
121.44029,31.194019
21
121.438139,31.190866
22
121.438239,31.190816
23
121.438339,31.190766
24
121.438039,31.190916
25
121.437939,31.190966
26
121.43992,31.194146
27
121.43982,31.194196
28
121.43972,31.194246
29
121.44002,31.194096
30
121.44012,31.194046
31
121.437803,31.194301
32
121.437903,31.194251
33
121.438003,31.194201
34
121.437703,31.194351
35
121.437603,31.194401
36
121.441537,31.18999
37
121.441537,31.19004
38
121.441537,31.19009
39
121.441537,31.18994
40
121.441537,31.18989
41
121.435616,31.195853
42
121.435516,31.195893
43
121.435416,31.195953
44
121.435716,31.195803
45
121.435816,31.195753
46
121.440356,31.190064
47
121.440256,31.190014
48
121.440156,31.189964
49
121.440456,31.190114
50
121.440556,31.190164
51
121.429155,31.191177
52
121.429055,31.191127
53
121.428955,31.191077
54
121.429255,31.191227
55
121.429355,31.191277
56
121.431103,31.199537
57
121.431003,31.199587
58
121.430903,31.199637
59
121.431203,31.199487
60
121.431303,31.199437
61
121.444074,31.194449
62
121.444174,31.194499
63
121.444274,31.194549
64
121.443874,31.194349
65
121.443974,31.194399
66
121.438035,31.19741
67
121.438135,31.19746
68
121.438235,31.19736
69
121.437935,31.19751
70
121.437835,31.19731
71
121.439556,31.19779
72
121.439456,31.19784
73
121.439356,31.19789
74
121.439656,31.19769
75
121.439756,31.19774
76
121.437098,31.190529
77
121.437198,31.190579
78
121.437298,31.190629
79
121.436998,31.190479
80
121.436898,31.190429
81
121.444342,31.191043
82
121.444442,31.191093
83
121.444542,31.191143
84
121.444242,31.190993
85
121.444142,31.190943
86
121.446028,31.191778
87
121.446128,31.191728
88
121.446228,31.191678
89
121.445928,31.191828
90
121.445828,31.191878
91
121.446264,31.192661
92
121.446364,31.192711
93
121.446464,31.192761
94
121.446164,31.192611
95
121.446064,31.192561
96
121.445941,31.193438
97
121.445841,31.193338
98
121.445741,31.193388
99
121.446041,31.193488
100
121.446141,31.193538
101
121.446733,31.193558
102
121.446833,31.193658
103
121.446933,31.193608
104
121.446633,31.193508
105
121.446533,31.193458
106
121.446357,31.194259
107
121.446257,31.194299
108
121.446157,31.194359
109
121.446457,31.194199
110
121.446557,31.194159
111
121.445276,31.194282
112
121.445176,31.194332
113
121.445076,31.194382
114
121.445376,31.194232
115
121.445476,31.194182
116
121.444074,31.194449
117
121.444174,31.194549
118
121.444274,31.194499
119
121.443974,31.194399
120
121.443874,31.194349
121
121.439408,31.195272
122
121.439508,31.195172
123
121.439608,31.195222
124
121.439308,31.195372
125
121.439208,31.195322
126
121.437884,31.194973
127
121.437784,31.195023
128
121.437684,31.195073
129
121.437984,31.194923
130
121.438084,31.194873
131
121.439096,31.195949
132
121.439196,31.195999
133
121.439296,31.196049
134
121.438996,31.195849
135
121.438896,31.195899
136
121.439216,31.19625
137
121.439316,31.1963
138
121.439416,31.19635
139
121.439116,31.1962
140
121.439016,31.19615
141
121.439974,31.193456
142
121.439974,31.193456
143
121.439974,31.193456
144
121.439974,31.193456
145
121.439974,31.193456
146
121.439034,31.195417
147
121.439134,31.195517
148
121.439234,31.195467
149
121.438934,31.195317
150
121.438834,31.195467
"""
np = ok.split('\n')
new_a = []
for i in np:
    if len(i) > 3:
        new_a.append(i)
print(new_a)

new_x = []
new_y = []
for i in new_a:
    tmp = i.split(',')
    new_x.append(float(tmp[0]))
    new_y.append(float(tmp[1]))
print(new_x)
print(new_y)

