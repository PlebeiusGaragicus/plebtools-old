    with output.put_loading(color='info'):
        if "tx" not in block:
            output.put_text(f"Block {height} has no transactions")
            return

        for txidx, tx in enumerate(block['tx']):
            for voutidx, vout in enumerate(tx['vout']): # THESE ARE THE UTXOs
                if 'scriptPubKey' in vout:
                    scriptPubKey = vout['scriptPubKey']
                    if "asm" in scriptPubKey:
                        asm = scriptPubKey["asm"]
                        if "OP_RETURN" in asm:
                            ophex = asm.replace("OP_RETURN ", "")
                            # require even number of characters (two hex digits per byte)
                            if len(ophex) % 2 == 1:
                                continue
                            # encodinglist = ["utf-8","gb18030","euc-kr","cp1253","utf-32","utf-16","euc-kr","cp1253","cp1252","iso8859-16","ascii","latin-1","iso8859-1"]
                            encodinglist = ["utf-8","ascii"]
                            hasError = True
                            try:
                                opbytes = bytes.fromhex(ophex)
                            except Exception as e:
                                logging.error(f"error handling ophex '{ophex}'")
                                logging.error(f"error is {e}")
                            for encoding in encodinglist:
                                if hasError == False:
                                    break
                                try:
                                    optext = opbytes.decode(encoding)
                                    # print(f"successfully converted with encoding {encoding}: {optext}")
                                    hasError = False
                                    # opreturns.append(optext)
                                    logging.debug(optext)
                                    logging.info(tx[{txidx}].vout[{voutidx}])
                                    output.put_markdown(f"## {optext}")
                                    # output.put_markdown(tx[{txidx}].vout[{voutidx}])
                                except Exception as e:
                                    print(f"error converting hex to text with encoding {encoding} for tx[{txidx}].vout[{voutidx}]: {e}")
                                    pass
        output.put_markdown(f"# END OF LIST")
