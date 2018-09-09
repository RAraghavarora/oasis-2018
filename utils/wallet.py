def transferHelper(data, type='transfer'):
    """
        Data must be a dictionary, this way it can easily be used by
        an API endpoint using request.data
        This function will take an amount and two wallet ids and transfer
        money between them. This helper function will reutrn a Response
        object if something is wrong with the requested data. So it's meant
        for views.
    """
    try:
        source = Wallet.objects.get(id=data["source-id"])
        target = Wallet.objects.get(id=data["target-id"])
        amount = data["amount"]
        if amount < 0:
            raise ValueError("amount transfered cannot be negative.")
            # log and handle accordingly - value error
        source.transferTo(target, amount, type=type)
        msg = {"message": "successful!"}
        return Response(msg, status=status.HTTP_200_OK)
    except KeyError as missing:
        msg = {"message": "missing the following field: {}".format(missing)}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    except Wallet.DoesNotExist:
        msg = {"message": "Wallet does not exist"}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
