from .twstock import gettwstock
import pprint
from .stocksAPI import stockapi
def wtd(query):
    if query[0:2] == '！ ' or query[0:2] == '! ':
        query = query[2:]

        ans = query
        return ans
    elif query[0:3] == 'tw ' or query[0:2] == 'TW ' or query[0:2] == 'Tw ':
        query = query[3:]
        query = str(query)
        query.split()
        ans = gettwstock(query)
        ans = str(ans)
        if 'Empty DataFrame' in ans:
            pass
        else:
            return ans

    elif query[0:3] == 'us ' or query[0:2] == 'US ' or query[0:2] == 'Us ':
        query = query[3:]
        ans = stockapi(query)
        return ans
    else:
        ans = None
        pass

# if __name__ == '__main__':

#     dis = wtd('us arkk')
#     print(dis)

#     pass