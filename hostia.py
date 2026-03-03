from dataclasses import dataclass, field
from typing import Dict, Optional

class AutentificacionError(Exception):
    pass

class FondosInsuficientes(Exception):
    pass

class MontoInvalido(Exception):
    pass

@dataclass
class Cuenta:
    numero: str
    titular: str
    pin: str
    saldo: float = field(default=0.0)

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise MontoInvalido("El monto a depositar debe de ser mayor q 0.")
        self.saldo += monto

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise MontoInvalido("El monto a retirar debe de ser mayor q 0.")
        if monto > self.saldo:
            raise FondosInsuficientes("No hay fondos suficientes")
        self.saldo -= monto


class Banco:
    def __init__(self) -> None:
        self._cuentas: Dict[str, Cuenta] = {}

    def agregar_cuenta(self, cuenta: Cuenta) -> None:
        if cuenta.numero in self._cuentas:
            raise ValueError("Ya existe una cuenta con este num.")
        self._cuentas[cuenta.numero] = cuenta

    def autenticar(self, numero: str, pin: str) -> Cuenta:
        cuenta = self._cuentas.get(numero)
        if not cuenta or cuenta.pin != pin:
            raise AutentificacionError("Numero de cuenta o PIN incorrecto")
        return cuenta


class Cajero:
    def __init__(self, banco: Banco) -> None:
        self.banco = banco
        self.cuenta_actual: Optional[Cuenta] = None

    def iniciar_sesion(self) -> None:
        print("==== Bienvenido al Cajero Automatico ====")
        while True:
            numero = input("Numero de cuenta (o Enter para cancelar): ").strip()
            if numero == "":
                print("Operacion Cancelada")
                return
            pin = input("PIN: ").strip()
            try:
                self.cuenta_actual = self.banco.autenticar(numero, pin)
                print(f"\n Autenticacion exitosa. Titular: {self.cuenta_actual.titular}\n")
                break

            except AutentificacionError as e:
                print(f"Ojo {e}\nIntenta de nuevo.\n")


    def mostar_menu(self) -> None:
        print("==== MENU ====")
        print("[1] Consultar Saldo")
        print("[2] Depositar")
        print("[3] Retirar")
        print("[4] Salir")

    def ejecutar_saldo(self) -> None:
        if not self.cuenta_actual:
            print("Debes Iniciar Sesion Primero")
            return

        while True:
            self.mostar_menu()
            opcion = input("Elige una opcion: ").strip()

            if opcion == "1":
                self.op_consultar()
            elif opcion == "2":
                self.op_depositar()
            elif opcion == "3":
                self.op_retirar()
            elif opcion == "4":
                print("Gracias por usar el Cajero ATM")
                break
            else:
                print("Operacion no valida")

    def op_consultar(self) -> None:
        print(f"\nSaldo actual: ${self.cuenta_actual.saldo:,.2f}\n")

    def op_depositar(self) -> None:
        try:
            monto = float(input("Ingrese el monto de depositar: "))
            self.cuenta_actual.depositar(monto)
            print(f"Deposito Exitoso. Saldo: ${self.cuenta_actual.saldo:,.2f}")

        except ValueError:
            print("Ingresa un numero valido\n")
        except MontoInvalido as e:
            print(f"Ojo {e}\n")

    def op_retirar(self) -> None:
        try:
            monto  = float(input("Ingrese el monto de retirar: "))
            self.cuenta_actual.retirar(monto)
            print(f"Retiro exitoso. Saldo: ${self.cuenta_actual.saldo:,.2f}")

        except ValueError:
            print("Ingresa un numero valido\n")
        except MontoInvalido as e:
            print(f"Ojo {e}\n")
        except FondosInsuficientes as e:
            print(f"Ojo {e}\n")

def probar_banco(banco: Banco) -> None:

    banco.agregar_cuenta(Cuenta(numero="1001", titular="Jose Shui", pin="1234", saldo=1500.00))
    banco.agregar_cuenta(Cuenta(numero="1002", titular="Luis Perez", pin="4567", saldo=500.00))
    banco.agregar_cuenta(Cuenta(numero="1003", titular="Daniel Ruiz", pin="0000", saldo=2500.00))

def main():
    banco = Banco()
    probar_banco(banco)

    cajero = Cajero(banco)
    cajero.iniciar_sesion()
    cajero.ejecutar_saldo()

if __name__ == '__main__':
    main()