from .lada_dmr import ProjectLadaDMR
from .lada_br import ProjectLadaBR
from .splaser import ProjectSplazer
from .coalition_pistol import CoalitionPistol
from .vesna_lsw import ProjectVesnaLSW
from .underbarrel_grenade_launcher import UnderbarrelGrenadeLauncher
from .basic_ammo import PlasmaChamber, EMChamber, APChamber
from .stat_mod_attachments import TelescopicSight, HolographicSight, Bipod, Suppressor
from .training import BasicTraining, SpecializedTraining
from .grenade_pack import GrenadePack


def LuminaDMR() -> ProjectLadaDMR:
    return (
        ProjectLadaDMR()
        .add_attachment(PlasmaChamber())
        .add_attachment(EMChamber())
        .add_attachment(APChamber())
        .add_attachment(TelescopicSight())
        .add_attachment(Bipod())
        .add_attachment(Suppressor())
        .add_attachment(SpecializedTraining())
    )


def LuminaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol()
        .add_attachment(HolographicSight())
        .add_attachment(Suppressor())
        .add_attachment(BasicTraining())
    )

def LuminaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo_count = {
            "Flashbang": (2, 2),
            "Concussion": (2, 2),
            "Fragmentation": (0, 0),
            "Smoke": (0, 0),
        },
    )


def GalinaBR() -> ProjectLadaBR:
    return (
        ProjectLadaBR()
        .add_attachment(Suppressor())
        .add_attachment(HolographicSight())
        .add_attachment(EMChamber())
        .add_attachment(PlasmaChamber())
        .add_attachment(APChamber())
        .add_attachment(SpecializedTraining())
    )


def GalinaSplaser() -> ProjectSplazer:
    return ProjectSplazer().add_attachment(BasicTraining())


def GalinaGrenadeLauncher() -> UnderbarrelGrenadeLauncher:
    return UnderbarrelGrenadeLauncher().add_attachment(BasicTraining())

def GalinaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo_count = {
            "Flashbang": (2, 2),
            "Concussion": (0, 0),
            "Fragmentation": (0, 0),
            "Smoke": (2, 2),
        },
    )

def SilviaLSW() -> ProjectVesnaLSW:
    return (
        ProjectVesnaLSW()
        .add_attachment(Bipod())
        .add_attachment(Suppressor())
        .add_attachment(HolographicSight())
        .add_attachment(PlasmaChamber())
        .add_attachment(EMChamber())
        .add_attachment(APChamber())
        .add_attachment(SpecializedTraining())
    )


def SilviaPistol() -> CoalitionPistol:
    return (
        CoalitionPistol()
        .add_attachment(HolographicSight())
        .add_attachment(Suppressor())
        .add_attachment(BasicTraining())
    )

def SilviaGrenades() -> GrenadePack:
    return GrenadePack(
        ammo_count = {
            "Flashbang": (2, 2),
            "Concussion": (0, 0),
            "Fragmentation": (0, 0),
            "Smoke": (2, 2),
        },
    )
