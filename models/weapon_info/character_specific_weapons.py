from .lada_dmr import ProjectLadaDMR
from .lada_br import ProjectLadaBR
from .splaser import ProjectSplazer
from .coalition_pistol import CoalitionPistol
from .vesna_lsw import ProjectVesnaLSW
from .underbarrel_grenade_launcher import UnderbarrelGrenadeLauncher
from .basic_ammo import PlasmaChamber, EMChamber, APChamber
from .stat_mod_attachments import TelescopicSight, HolographicSight, Bipod, Suppressor, VerticalGrip
from .training import BasicTraining, SpecializedTraining
from .grenade_pack import GrenadePack
from .siren_knife import SirenKnife
from .lada_smg import ProjectLadaSMG


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
            "Flashbang": (2, 4),
            "Concussion": (2, 4),
            "Fragmentation": (0, 4),
            "Smoke": (0, 4),
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
            "Flashbang": (2, 4),
            "Concussion": (0, 4),
            "Fragmentation": (0, 4),
            "Smoke": (2, 4),
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
            "Flashbang": (2, 4),
            "Concussion": (0, 4),
            "Fragmentation": (0, 4),
            "Smoke": (2, 4),
        },
    )


def Knife() -> SirenKnife:
    return SirenKnife().add_attachment(
        BasicTraining()
    )

def ReplacementSMG() -> ProjectLadaSMG:
    ret =  ProjectLadaSMG().add_attachment(
        BasicTraining()
    ).add_attachment(PlasmaChamber()).add_attachment(
        HolographicSight()
    ).add_attachment(
        Suppressor()
    ).add_attachment(
        VerticalGrip()
    ).replace_magazine("FMJ", "Plasma").replace_magazine("FMJ", "Plasma").replace_magazine("FMJ", "Plasma")
    ret.switch_ammo()
    return ret

