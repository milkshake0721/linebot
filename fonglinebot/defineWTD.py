def wtd(query):
    if query[0] == '！' or query[0] == '!':
        ans = 'b'
        return ans
    else:
        ans = 'c'
        return ans

if __name__ == '__main__':

    dis = wtd('ja')
    print(dis)

    pass