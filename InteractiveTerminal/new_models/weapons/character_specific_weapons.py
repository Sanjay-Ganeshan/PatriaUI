from .lada_dmr import ProjectLadaDMR
from .lada_br import ProjectLadaBR
from .splazer import Splazer
from .coalition_pistol import CoalitionPistol
from .ammo_pack import AmmoPack
from .vesna_lsw import ProjectVesnaLSW
from .underbarrel_grenade_launcher import UnderbarrelGrenadeLauncher
from .basic_ammo import PlasmaChamber, EMChamber, APChamber
from .stat_mod_attachments import TelescopicSight, HolographicSight, Bipod, Suppressor, VerticalGrip
from .training import BasicTraining, SpecializedTraining
from .grenade_pack import GrenadePack
from .siren_knife import SirenKnife
from .lada_cq import ProjectLadaCQ
from .exp_shotgun import ExperimentalShotgun
from .lada_sniper import ProjectLadaSniper
from .switchblade import SwitchbladeDrone
from ...utils import CircularList


def LuminaDMR() -> ProjectLadaDMR:
    return (
        ProjectLadaDMR().add_attachment(PlasmaChamber()).add_attachment(
            EMChamber()
        ).add_attachment(APChamber()).add_attachment(
            TelescopicSight()
        ).add_attachment(Bipod()).add_attachment(Suppressor()).add_attachment(
            SpecializedTraining()
        )
    )


def LuminaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol().add_attachment(HolographicSight()).add_attachment(
            Suppressor()
        ).add_attachment(BasicTraining())
    )


def LuminaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Concussion",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Smoke",
                    current=0,
                    capacity=0,
                )
            ]
        )
    )


def GalinaBR() -> ProjectLadaBR:
    return (
        ProjectLadaBR().add_attachment(Suppressor()).add_attachment(
            HolographicSight()
        ).add_attachment(EMChamber()).add_attachment(
            PlasmaChamber()
        ).add_attachment(APChamber()).add_attachment(SpecializedTraining())
    )


def GalinaSplaser() -> Splazer:
    return Splazer().add_attachment(BasicTraining())


def GalinaGrenadeLauncher() -> UnderbarrelGrenadeLauncher:
    return UnderbarrelGrenadeLauncher().add_attachment(BasicTraining())


def GalinaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Concussion",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Smoke",
                    current=2,
                    capacity=2,
                )
            ]
        )
    )


def SilviaLSW() -> ProjectVesnaLSW:
    return (
        ProjectVesnaLSW().add_attachment(Bipod()).add_attachment(
            Suppressor()
        ).add_attachment(HolographicSight()).add_attachment(
            PlasmaChamber()
        ).add_attachment(EMChamber()).add_attachment(
            APChamber()
        ).add_attachment(SpecializedTraining())
    )


def SilviaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol().add_attachment(HolographicSight()).add_attachment(
            Suppressor()
        ).add_attachment(BasicTraining())
    )


def SilviaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Concussion",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Smoke",
                    current=2,
                    capacity=2,
                )
            ]
        )
    )


def Knife() -> SirenKnife:
    return SirenKnife().add_attachment(BasicTraining())


def ReplacementSMG() -> ProjectLadaCQ:
    ret = ProjectLadaCQ().add_attachment(BasicTraining()).add_attachment(
        PlasmaChamber()
    ).add_attachment(HolographicSight()).add_attachment(
        Suppressor()
    ).add_attachment(VerticalGrip()).replace_magazine(
        "FMJ", "Plasma"
    ).replace_magazine("FMJ", "Plasma").replace_magazine("FMJ", "Plasma")
    return ret

def ElenaShotgun() -> ExperimentalShotgun:
    return (
        ExperimentalShotgun().add_attachment(
            Suppressor()
        #yes, you can suppress a shotgun - bit difficult in 2023, but doable in 2621
        ).add_attachment(HolographicSight()
        ).add_attachment(EMChamber()
        ).add_attachment(SpecializedTraining())
    )

def ElenaDrone() -> SwitchbladeDrone:
    return SwitchbladeDrone().add_attachment(BasicTraining())

def ElenaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Concussion",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Smoke",
                    current=0,
                    capacity=0,
                )
            ]
        )
    )

def RivkaSniper() -> ProjectLadaSniper:
    return (
        ProjectLadaSniper().add_attachment(PlasmaChamber()).add_attachment(
            EMChamber()
        ).add_attachment(APChamber()).add_attachment(
            TelescopicSight()
        ).add_attachment(Bipod()).add_attachment(Suppressor()).add_attachment(
            SpecializedTraining()
        )
    )

def RivkaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol().add_attachment(HolographicSight()).add_attachment(
            Suppressor()
        ).add_attachment(BasicTraining())
    )

def RivkaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Concussion",
                    current=2,
                    capacity=2,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=0,
                    capacity=0,
                ),
                AmmoPack(
                    name="Smoke",
                    current=0,
                    capacity=0,
                )
            ]
        )
    )

def OpheliaShotgun() -> ExperimentalShotgun:
    return (
        ExperimentalShotgun()
            .add_attachment(Suppressor())
            .add_attachment(HolographicSight())
            .add_attachment(APChamber())
            .add_attachment(PlasmaChamber())
            .add_attachment(SpecializedTraining())
    )

def OpheliaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol()
            .add_attachment(BasicTraining())
            .add_attachment(HolographicSight())
            .add_attachment(Suppressor())
    )

def OpheliaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Concussion",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Smoke",
                    current=1,
                    capacity=1,
                )
            ]
        )
    )

def PilviGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Concussion",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Smoke",
                    current=1,
                    capacity=1,
                )
            ]
        )
    )


def PilviBR() -> ProjectLadaBR:
    return (
        ProjectLadaBR().add_attachment(Suppressor()).add_attachment(
            HolographicSight()
        ).add_attachment(EMChamber()).add_attachment(
            PlasmaChamber()
        ).add_attachment(APChamber()).add_attachment(SpecializedTraining())
    )

def PilviGrenadeLauncher() -> UnderbarrelGrenadeLauncher:
    return UnderbarrelGrenadeLauncher().add_attachment(BasicTraining())

def PilviPistol() -> CoalitionPistol:
    return (
        CoalitionPistol().add_attachment(HolographicSight()).add_attachment(
            Suppressor()
        ).add_attachment(BasicTraining())
    )

def ZoeLSW() -> ProjectVesnaLSW:
    return (
        ProjectVesnaLSW().add_attachment(Bipod()).add_attachment(
            Suppressor()
        ).add_attachment(HolographicSight()).add_attachment(
            PlasmaChamber()
        ).add_attachment(EMChamber()).add_attachment(
            APChamber()
        ).add_attachment(SpecializedTraining())
    )


def ZoePistol() -> CoalitionPistol:
    return (
        CoalitionPistol().add_attachment(HolographicSight()).add_attachment(
            Suppressor()
        ).add_attachment(BasicTraining())
    )


def ZoeGrenades() -> GrenadePack:
    return GrenadePack(
        ammo=CircularList(
            items=[
                AmmoPack(
                    name="Flashbang",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Concussion",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Fragmentation",
                    current=1,
                    capacity=1,
                ),
                AmmoPack(
                    name="Smoke",
                    current=1,
                    capacity=1,
                )
            ]
        )
    )