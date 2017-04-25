import sys
print sys.version
import time

def print_sbar(n,m,s='[|.]',size=100):
    '''(int,int,string,int) -> None
    Print a progress bar using the simbols in 's'.
    Example:
            print '\nfor n in range():'
            m = 30
            for n in range(m):
                time.sleep(0.1)
                print_sbar(n+1,m,s='|#.|',size=40)

            print '\nwhile n:'
            x = 30
            while x:
                time.sleep(0.1)
                print_sbar(n=30-x,m=30-1,s='|> |',size=40)
                x -= 1

            print '\ndone'

    Output:
            for n in range():
            |########################################| 100.0%
            while n:
            |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100.0%
    '''
    #convert inputs to float
    n = float(n)
    m = float(m)
    size = float(size)
    #adjust to bar size
    if m != size:
        n =(n*size)/m
        m = size
    #calculate ticks
    _a = int(n)*s[1]+(int(m)-int(n))*s[2]
    _b = round(n/(int(m))*100,1)
    #adjust overflow
    if _b > 100:
        _b = 100.0
    #to stdout    
    sys.stdout.write('\r{}{}{} {}%'.format(s[0],_a,s[3],_b))
    sys.stdout.flush()


