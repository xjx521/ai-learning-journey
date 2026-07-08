import pickle

x,y,z=1,2,3
s="fishc"
l=["牛逼",520,1314]
d={"one":1,"two":2}

with open("data.pkl","wb") as f:
    pickle.dump(x,f)#pickle.dump((x,y,z,s,l,d),f)
    pickle.dump(y,f)
    pickle.dump(z,f)
    pickle.dump(s,f)
    pickle.dump(l,f)
    pickle.dump(d,f)
