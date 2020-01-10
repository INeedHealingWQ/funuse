static int stfunc(int v)
{
    return v;
}

int func()
{
    stfunc(6);
    return 0;
}
