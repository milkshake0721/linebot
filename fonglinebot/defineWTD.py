from .twstock import gettwstock
import pprint
from .stocksAPI import stockapi
def wtd(query):
    if query[0:3] == 'tw ' or query[0:3] == 'TW ' or query[0:3] == 'Tw ':
        query = query[3:]
        query = str(query)

        ans = gettwstock(query)
        ans = str(ans)
        if 'Empty DataFrame' in ans:
            pass
        else:
            return ans

    elif query[0:3] == 'us ' or query[0:3] == 'US ' or query[0:3] == 'Us ':
        query = query[3:]
        ans = stockapi(query)
        return ans

    elif query == '匯率':
        ans = currency()
        return ans

    else:
        ans = None
        pass

# if __name__ == '__main__':

#     dis = wtd('Tw 2330')
#     print(dis)

#     pass