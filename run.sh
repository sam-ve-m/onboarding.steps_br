echo "- Applying specs..."; fission spec apply || { echo "ERROR: Failed to apply spec. [FINISHING SCRIPT]"; exit; }
echo "- Making port accessible outside the cluster..."; kubectl --namespace fission port-forward $(kubectl --namespace fission get pod -l svc=router -o name) $FISSION_TCP_PORT:8888 &
export FISSION_ROUTER=127.0.0.1:$FISSION_TCP_PORT