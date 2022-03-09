from twstock import gettwstock
import pprint
def wtd(query):
    if query[0:2] == '！ ' or query[0:2] == '! ':
        query = query[2:]

        ans = query
        return ans
    elif query[0:2] == 'tw' or query[0:2] == 'TW' or query[0:2] == 'Tw':
        query = query[3:]
        query = str(query)
        query.split()
        ans = gettwstock(query)
        return ans
    else:
        ans = None
        return ans

# if __name__ == '__main__':

#     dis = wtd('tw 2330')
#     print(dis)

#     pass