import subprocess
from Cryptodome.Util.number import long_to_bytes
iv_c1_c2_c3='4e9bd8fb5331702fb4a7ea7e0b9ec3370e4ac53f9f569e53ccb0e035f9c8ed4fddc0f0c4e4d41b2d3b70a1d73fa6d7f53ac4758c8e179d4a1f1a47978c879205'
iv=iv_c1_c2_c3[:32]
c1=iv_c1_c2_c3[32:64]
c2=iv_c1_c2_c3[64:96]
c3=iv_c1_c2_c3[96:]
b=16
#进一步得到a_j-1
def huifu(j,r,y,y_o):
    r_k=''
    for i in range(j-1,b):#设置r_k……
        r_k+=hex(int(y[2*i:2*(i+1)],16)^(b-j+2))[2:].rjust(2,'0')
        print('r_k',r_k)
    #print('y',y)
    for k in range(0x00,0x100):#穷搜r_j-1
        r_j1=hex(k)[2:].rjust(2,'0')
        r_new=r[:2*(j-2)]+r_j1+r_k
        #print('r_new',r_new)
        daiyanzheng=r_new+y_o
        result=subprocess.call([r'C:\Users\Lenovo\Desktop\12\dec_oracle.exe',daiyanzheng])
        if (result==200):
            y_j1=hex(int(r_j1,16)^ (b-j+2))[2:].rjust(2,'0')#更新a_j-1
            y=y[:2*(j-2)]+y_j1+y[2*(j-1):]
            return y    
#求解
def jie(r,yy):
    r_o=r
    y_o=yy
    rr=r[:30]
    #找到满足上式的r
    for i in range(0x00,0x100):#穷搜r_b
        r_b=hex(i)[2:].rjust(2,'0')
        rrr=rr+r_b
        daiyanzheng=rrr+yy
        result=subprocess.call([r'C:\Users\Lenovo\Desktop\12\dec_oracle.exe',daiyanzheng])
        if (result==200):
            rr=rrr
            break
    #print("找到上式r",rrr)
    #进一步判断填充的长度
    j=0
    for k in range(b):
        r_j='00'#修改的r_j
        daiyanzheng=rr[:2*k]+r_j+rr[2*(k+1):]+yy
        result=subprocess.call([r'C:\Users\Lenovo\Desktop\12\dec_oracle.exe',daiyanzheng])
        if (result==500):
            j=k+1#求出j
            break
    #print('j',j)
    #根据填充规则计算a_j->a_b
    tc=b-j+1#填充字节数量
    y_new=''
    for u in range(j-1,b):
        y_new+=hex(int(rr[2*u:2*(u+1)],16)^tc)[2:].rjust(2,'0')
    yy=yy[:2*(j-1)]+y_new
    print('y_new',y_new,'yy',yy)
    for n in range(j-1):
        yy=huifu(j-n,rr,yy,y_o)
    p=hex(int(yy,16)^int(r_o,16))[2:]
    return p    
p3=jie(c2,c3)
p2=jie(c1,c2)
p1=jie(iv,c1)
pp=int((p1+p2+p3),16)
print(long_to_bytes(pp))
        
        
        
        
        
    
        
            
            
        
        
    

