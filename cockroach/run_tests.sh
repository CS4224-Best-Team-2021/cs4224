seq=("new-order" "payment" "delivery" "order-status" "stock-level" "popular-item" "top-balance" "related-customer")

for i in ${seq[@]}; do
    echo "running $i"
    bash app.sh < crosscheck/$i.in > crosscheck/$i.out
done