Transaction Workload B

Order-status: 
- Sorting of orders of a customer                   => Index on Order.O_ENTRY_D
- Obtain each item in the customer's last order     => Potentially denormalize Order and Order-Line

Stock-level + Popular-item:
- Sorting of Order.O_ENTRY_D        => Index on Order.O_ENTRY_D
- Joining Order and Order-Line      => Potentially denormalize Order and Order-Line

Top-balance:
- Sorting of Customer.C_BALANCE DESC    => Index on Customer.C_BALANCE

Related-customer:
- Nested EXISTS clauses     => Potentially might have benefits of denormalize Order and Order-Line