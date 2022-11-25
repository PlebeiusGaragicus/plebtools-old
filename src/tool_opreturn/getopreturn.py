def getblockopreturns(blocknum):

    b = getblock(blocknum, 2)
    opreturns = []
    if "tx" in b:
        txidx = 0
        for tx in b["tx"]:
            txidx += 1
            voutidx = 0
            if "vout" in tx:
                for vout in tx["vout"]:
                    voutidx += 1
                    if "scriptPubKey" in vout:
                        scriptPubKey = vout["scriptPubKey"]
                        if "asm" in scriptPubKey:
                            asm = scriptPubKey["asm"]
                            if "OP_RETURN" in asm:
                                ophex = asm.replace("OP_RETURN ", "")
                                # require even number of characters
                                if len(ophex) % 2 == 1:
                                    continue
                                # require more than one word
#                                if "20" not in ophex:
#                                    continue
                                #encodinglist = ["utf-8","gb18030","euc-kr","cp1253","utf-32","utf-16","euc-kr","cp1253","cp1252","iso8859-16","ascii","latin-1","iso8859-1"]
                                encodinglist = ["utf-8","ascii"]
                                hasError = True
                                try:
                                    opbytes = bytes.fromhex(ophex)
                                except Exception as e:
                                    print(f"error handling ophex '{ophex}'")
                                    print(f"error is {e}")
                                for encoding in encodinglist:
                                    if hasError == False:
                                        break
                                    try:
                                        optext = opbytes.decode(encoding)
                                        print(f"successfully converted with encoding {encoding}: {optext}")
                                        hasError = False
                                        opreturns.append(optext)
                                    except Exception as e:
#                                        print(f"error converting hex to text with encoding {encoding} for tx[{txidx}].vout[{voutidx}]: {e}")
                                        pass