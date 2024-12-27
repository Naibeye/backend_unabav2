
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from hashlib import sha256
from ellipticcurve.signature import Signature
from ellipticcurve.math import Math
from ellipticcurve.utils.integer import RandomInteger
from ellipticcurve.utils.binary import numberFromByteString
from ellipticcurve.utils.compatibility import *
from ellipticcurve.curve import secp256k1
from json import dumps, loads
import math, random
from .otp import base64_to_string, string_to_base64, OTP
 
# function to generate OTP
def generateOTP(nbreDigits=4) :
 
    # Declare a digits variable  
    # which stores all digits 
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    while len(OTP)!=6:
        for i in range(nbreDigits) :
            OTP += digits[math.floor(random.random() * 10)]
    return int(OTP)

class Authentication:
    @classmethod
    def hash2number(cls,text, hashfunc=sha256 ):
        byteMessage = hashfunc(bytes(string_to_base64(text).encode("utf-8"))).digest()
        numberMessage = numberFromByteString(byteMessage)
        return numberMessage

    @classmethod
    def validation(cls, data,  privateKeyIP, hashfunc=sha256):
        curve = privateKeyIP.curve
        public_key_ip=privateKeyIP.publicKey()
        public_key_cert=PublicKey.fromPem(base64_to_string(data['publicKeyCert']))
        public_key=PublicKey.fromPem(data['public_key'])
        resdata = data['mail']+data['name']+data['publicKeyCert']
        byteMessage = hashfunc(bytes(string_to_base64(resdata).encode("utf-8"))).digest()
        numberMessage = numberFromByteString(byteMessage)
        publicKeyPrime= PublicKey(Math.add(public_key_cert.point, Math.multiply(public_key_ip.point, numberMessage, N=curve.N,A=curve.A, P=curve.P), A=curve.A, P=curve.P), curve)
        return publicKeyPrime.toPem()== public_key.toPem(), public_key.toPem()

    @classmethod
    def registration(cls , data,  privateKeyIP, hashfunc=sha256):
        """
        The `registration` function generates a secret key and identity hash for a given name, email,
        public key, and private key.
        
        :param cls: In the provided code snippet, the `registration` function takes several parameters.
        Here's a breakdown of what each parameter represents:
        :param name: The `name` parameter in the `registration` function is a string that represents the
        name of the entity or user for whom the registration is being done
        :param mail: The `mail` parameter in the `registration` function represents the email address of
        the user who is registering. It is used as part of the identity information for hashing and
        generating the secret key during the registration process
        :param publicKey: It seems like the information about the `publicKey` parameter is missing in
        your message. Could you please provide more details or specify what you would like to know about
        the `publicKey` parameter in the `registration` function?
        :param privateKeyIP: The `privateKeyIP` parameter in the `registration` function seems to
        represent a private key associated with an elliptic curve cryptography (ECC) key pair. It is
        used for generating a digital signature during the registration process. The function takes this
        private key as input along with other parameters like `
        :param hashfunc: The `hashfunc` parameter in the `registration` function is a function that
        represents a cryptographic hash function. In this case, the default hash function being used is
        SHA-256 (Secure Hash Algorithm 256-bit)
        :return: The function `registration` returns a tuple containing two values: `secret` and the
        serialized identity information `identityForHash`.
        """

        curve = privateKeyIP.curve
        publicKey=PublicKey.fromPem(data['public_key'])
        randNum = RandomInteger.between(1, curve.N - 1)
        randPoint = Math.multiply(curve.G, n=randNum, A=curve.A, P=curve.P, N=curve.N)
        publicKeyCert= PublicKey(Math.add(randPoint, publicKey.point, A=curve.A, P=curve.P), curve)
        del data['public_key']
        data.update({'publicKeyCert':string_to_base64(publicKeyCert.toPem())})
        resdata = data['mail']+data['name']+data['publicKeyCert']
        byteMessage = hashfunc(bytes(string_to_base64(resdata).encode("utf-8"))).digest()
        numberMessage = numberFromByteString(byteMessage)
        code=generateOTP(6)
        secret=(code*(randNum + numberMessage * privateKeyIP.secret))  % curve.N
        return PrivateKey(curve, secret).toPem(), code, data
    
    @classmethod
    def verify(cls,data,secretVerifier, identityVerifier,  hashfunc=sha256):
        """
        The function `verify` takes in various parameters, performs cryptographic operations, and
        returns a boolean value based on the comparison of two public keys.
        
        :param cls: It seems like the code snippet you provided is a method named `verify` that takes
        several parameters and performs some cryptographic operations. However, you have not provided
        the definition or context of the `cls` parameter in this function
        :param prover: The `verify` function you provided seems to be a cryptographic verification
        function. The `prover` parameter is expected to be a serialized object that contains information
        needed for the verification process
        :param privateKeyVerifier: The `privateKeyVerifier` parameter in the `verify` function is used
        as the private key for verification purposes. It is expected to be in PEM format and is
        converted to a `PrivateKey` object using the `fromPem` method. This private key is then used in
        various mathematical operations within
        :param publicKeyEPProver: The `publicKeyEPProver` parameter in the `verify` function is expected
        to be a public key in PEM format that belongs to the prover. This public key is used in various
        cryptographic operations within the function to verify certain conditions
        :param K: It seems like the code snippet you provided is a method for verifying some
        cryptographic operations. The parameter `K` is used in the code snippet as a variable
        representing a value that is used in the cryptographic calculations. The specific purpose or
        origin of this value is not clear from the provided code snippet alone
        :param publicKeyIP: The `publicKeyIP` parameter in the `verify` function represents the public
        key associated with the Identity Provider (IP). This key is used in cryptographic operations
        within the function to verify the authenticity and integrity of the data being processed
        :param hashfunc: The `hashfunc` parameter in the `verify` function is used to specify the hash
        function that will be used for hashing data. In the provided code snippet, the default hash
        function used is `sha256`, which is a common cryptographic hash function that produces a 256-bit
        (32-byte)
        :return: a boolean value indicating whether the variable `KPPem` is equal to `KPPrimePem`.
        """
       
        try:
            identityVerifierObject=loads(base64_to_string(identityVerifier+"="))
            public_key_ip =PublicKey.fromPem(base64_to_string(identityVerifierObject['public_key_ip']))
            curve=public_key_ip.curve
            privateKey=PrivateKey(curve,int(base64_to_string(secretVerifier)))
            publicKeyEP=PublicKey.fromPem(base64_to_string(data['publicKeyEp']))
            GPrime=PublicKey(Math.multiply(publicKeyEP.point, privateKey.secret,curve.N, curve.A, curve.P), curve)
            key=OTP.generate_key_from_password(GPrime.toDer())
            dataDecrypt=loads(OTP.decrypt(data['data'], key.encode("utf-8")))
            K=dataDecrypt['K']
            KprivateKey=PrivateKey(curve, int(K))
            KPPem=KprivateKey.publicKey().toPem()
            proverIdentity=loads(base64_to_string(dataDecrypt['proverIdentity']))
            resProverSession = proverIdentity['mail']+proverIdentity['name']+proverIdentity['publicKeyCert']+data['publicKeyEp']
            byteMessage = hashfunc(bytes(string_to_base64(resProverSession).encode("utf-8"))).digest()
            numberProverSession = numberFromByteString(byteMessage)
            HX=Math.multiply(publicKeyEP.point, numberProverSession,curve.N, curve.A, curve.P, )
            resdataProver = string_to_base64(proverIdentity['mail']+proverIdentity['name']+proverIdentity['publicKeyCert'])
            byteMessage = hashfunc(bytes(resdataProver.encode("utf-8"))).digest()
            numberMessageProver = numberFromByteString(byteMessage)
            publicKeyCert = PublicKey.fromPem(base64_to_string(proverIdentity['publicKeyCert']))
            publicKey=Math.add(publicKeyCert.point, Math.multiply(public_key_ip.point, numberMessageProver, curve.N, curve.A, curve.P), curve.A, curve.P)
            publicKeyPem=PublicKey(publicKey, curve).toPem()
            KPPrime=Math.add(publicKey,HX ,curve.A, curve.P)
            KPPrimePem=PublicKey(KPPrime, curve).toPem()
            if string_to_base64(KPPrimePem)== string_to_base64(KPPem):
                print(f'{int(key):0x}')
                return {**dataDecrypt, "_id":f"{numberMessageProver:0x}", "proverIdentity": proverIdentity, "token": f'{int(key):0x}' }
            else:
                return None
        except Exception as e:
            print(e)
            return None
