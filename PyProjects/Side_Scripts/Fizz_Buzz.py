def FizzBuzz(num):
    answer=''
    for x in range(1,num+1):
        if x%3 == 0:
            answer+='Fizz'
        if x%5 == 0:
            answer+='Buzz'
        if x%3 !=0 and x%5 !=0:
            answer+=str(x)
        answer+=' '
    return answer


print(FizzBuzz(50))
