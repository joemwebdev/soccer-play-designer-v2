from xml.etree import ElementTree as ET


def color(r,g,b,a=1):
    return f'<color><r>{r:.6f}</r><g>{g:.6f}</g><b>{b:.6f}</b><a>{a:.6f}</a></color>'

def vec(x,y):
    return f'<vector><x>{x:.6f}</x><y>{y:.6f}</y></vector>'

def anim_vec(points):
    return '<animated type="vector">' + ''.join(
        f'<waypoint time="{t}" before="auto" after="auto">{vec(x,y)}</waypoint>' for t,x,y in points
    ) + '</animated>'

def anim_real(points):
    return '<animated type="real">' + ''.join(
        f'<waypoint time="{t}" before="auto" after="auto"><real value="{v:.6f}"/></waypoint>' for t,v in points
    ) + '</animated>'

def circle(desc,r,g,b,radius,origin,amount=None):
    amount = amount or '<real value="1.0"/>'
    return f'''<layer type="circle" active="true" version="0.1" desc="{desc}">
<param name="z_depth"><real value="0"/></param><param name="amount">{amount}</param>
<param name="blend_method"><integer value="0"/></param><param name="color">{color(r,g,b)}</param>
<param name="radius"><real value="{radius}"/></param><param name="feather"><real value="0"/></param>
<param name="origin">{origin}</param><param name="invert"><bool value="false"/></param>
<param name="falloff"><integer value="1"/></param></layer>'''

def rect(desc,r,g,b,p1,p2):
    return f'''<layer type="rectangle" active="true" version="0.2" desc="{desc}">
<param name="z_depth"><real value="0"/></param><param name="amount"><real value="1"/></param>
<param name="blend_method"><integer value="0"/></param><param name="color">{color(r,g,b)}</param>
<param name="point1">{p1}</param><param name="point2">{p2}</param>
<param name="expand"><real value="0"/></param><param name="invert"><bool value="false"/></param></layer>'''

head=[('0s',0,1.25),('1.5s',-.08,1.30),('3s',.03,1.18),('4.2s',.08,1.22),('5.5s',.18,1.35),('7s',0,1.28)]
eye_l=[(t,x-.38,y+.08) for t,x,y in head]
eye_r=[(t,x+.38,y+.08) for t,x,y in head]
hair=[(t,x,y+.05) for t,x,y in head]
pupil_l=[('0s',-.32,1.33),('1.5s',-.42,1.36),('3s',-.24,1.24),('4.2s',-.18,1.29),('5.5s',-.13,1.44),('7s',-.25,1.36)]
pupil_r=[('0s',.44,1.33),('1.5s',.34,1.36),('3s',.52,1.24),('4.2s',.58,1.29),('5.5s',.63,1.44),('7s',.51,1.36)]
blink=anim_real([('0s',1),('1.35s',1),('1.43s',0),('1.52s',1),('5.10s',1),('5.18s',0),('5.28s',1),('7s',1)])

hand=[('0s',1.35,-.05),('2s',1.35,-.05),('3.1s',.95,.85),('4.2s',.95,.85),('5s',1.25,.20),('7s',1.25,.20)]
mug1=[('0s',.78,.35),('2s',.78,.35),('3.1s',.38,1.25),('4.2s',.38,1.25),('5s',.68,.60),('7s',.68,.60)]
mug2=[('0s',1.52,-.45),('2s',1.52,-.45),('3.1s',1.12,.45),('4.2s',1.12,.45),('5s',1.42,-.20),('7s',1.42,-.20)]
arm1=[('0s',.95,-.35),('2s',.95,-.35),('3.1s',.55,.55),('4.2s',.55,.55),('5s',.85,-.10),('7s',.85,-.10)]
arm2=[('0s',1.35,-1.55),('2s',1.35,-1.55),('3.1s',.95,-.65),('4.2s',.95,-.65),('5s',1.25,-1.30),('7s',1.25,-1.30)]
handle=[('0s',1.57,-.03),('2s',1.57,-.03),('3.1s',1.17,.87),('4.2s',1.17,.87),('5s',1.47,.22),('7s',1.47,.22)]

def follow(dx1,dy1,dx2,dy2):
    return anim_vec([(t,x+dx1,y+dy1) for t,x,y in head]), anim_vec([(t,x+dx2,y+dy2) for t,x,y in head])

layers=[]
layers += [
 circle('Right hand',.92,.57,.40,.28,anim_vec(hand)),
 rect('Mug body',.97,.97,.94,anim_vec(mug1),anim_vec(mug2)),
 circle('Mug handle',.97,.97,.94,.27,anim_vec(handle)),
 circle('Left eye',1,1,1,.19,anim_vec(eye_l),blink), circle('Right eye',1,1,1,.19,anim_vec(eye_r),blink),
 circle('Left pupil',.18,.09,.04,.085,anim_vec(pupil_l),blink), circle('Right pupil',.18,.09,.04,.085,anim_vec(pupil_r),blink)
]
b1,b2=follow(-.58,.39,-.18,.32); layers.append(rect('Left brow',.12,.045,.025,b1,b2))
b1,b2=follow(.18,.32,.58,.39); layers.append(rect('Right brow',.12,.045,.025,b1,b2))
layers += [circle('Mouth',.55,.16,.18,.13,anim_vec([(t,x,y-.42) for t,x,y in head])),
           circle('Face',.92,.58,.41,.95,anim_vec(head)),
           circle('Front hair',.16,.055,.025,1.05,anim_vec([(t,x,y+.25) for t,x,y in head])),
           rect('Right forearm',.92,.57,.40,anim_vec(arm1),anim_vec(arm2)),
           circle('Right sleeve',.08,.075,.085,.62,vec(.95,-1.25)), circle('Left sleeve',.08,.075,.085,.62,vec(-.95,-1.25)),
           rect('Torso',.08,.075,.085,vec(-1.35,-.35),vec(1.35,-3.10)), rect('Neck',.92,.57,.40,vec(-.28,.15),vec(.28,-.55)),
           circle('Hair back',.11,.035,.018,1.28,anim_vec(hair)),
           rect('Counter',.72,.53,.42,vec(-3,-2.90),vec(3,-5.333)), rect('Window light',.93,.81,.66,vec(-2.7,4.7),vec(-.9,.8)),
           rect('Background',.90,.79,.67,vec(-3,5.333),vec(3,-5.333))]

sif=f'''<?xml version="1.0"?>
<canvas version="1.0" width="540" height="960" xres="2834.645752" yres="2834.645752" view-box="-3 5.333333 3 -5.333333" antialias="1" fps="30" begin-time="0f" end-time="7s" bgcolor="0.9 0.79 0.67 1">
<name>MILA Synfig Proof of Concept</name><desc>Vector rig movement test: blink, gaze, head motion, mug lift and reaction.</desc>{''.join(layers)}</canvas>'''
ET.fromstring(sif)
open('mila-animation/mila_poc.sif','w',encoding='utf-8').write(sif)
print('Generated mila-animation/mila_poc.sif')
