long get_random(void)

{
  int iVar1;
  
  iVar1 = rand();
  return (long)(iVar1 % 100);
}