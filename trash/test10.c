typedef struct test_struct
{
    int a;
    int b;
} test_struct;

int func(void *arg)
{
    test_struct *st;
    st = (test_struct *)arg;
    return 0;
}
