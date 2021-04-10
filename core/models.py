from django.db import models

BENEFIT_TYPE = (
    (1, u'Скидка'),
    (2, u'Деньги'),
    (3, u'Другое'),
)

PERIODICITY = (
    (1, u'Раз в месяц'),
    (2, u'Раз в год'),
    (3, u'Единовремено'),
)

SIGN = (
    (1, u'Больше'),
    (2, u'Меньше'),
    (3, u'Равно'),
)

class BenefitsType(models.Model):

    """
    Тип льгот
    """

    title = models.CharField(max_length=512, verbose_name=u'Заголовок')

    def __str__(self):
        return str(self.title)

    class Meta:

        verbose_name = u'Тип льгот'
        verbose_name_plural = u'Типы льгот'


class InformationDocuments(models.Model):

    """
    Документы, информирующие о льготах
    """

    title = models.CharField(max_length=512, verbose_name=u'Загаловок')
    link = models.TextField(verbose_name=u'Ссылка на документ')


    def __str__(self):
        return str(self.title)

    class Meta:

        verbose_name = u'Информирующий документ'
        verbose_name_plural = u'Информирующие документы'


class RequiredDocuments(models.Model):

    """
    Документы, требуемые для получения льгот
    """

    title = models.CharField(max_length=512, verbose_name=u'Загаловок')
    description = models.TextField(verbose_name=u'Описание документа')


    def __str__(self):
        return str(self.title)

    class Meta:

        verbose_name = u'Требуемый документ'
        verbose_name_plural = u'Требуемые документы'

class Benefit(models.Model):

    """
    Общий список всех льгот
    """

    title = models.CharField(max_length=512, verbose_name=u'Заголовок')
    type = models.IntegerField(verbose_name=u'Тип льготы', default=3, choices=BENEFIT_TYPE)
    value = models.CharField(max_length=512, verbose_name=u'Значение', blank=True)
    start_date = models.DateField(verbose_name=u'Дата начала действия льготы', auto_now_add=True)
    end_date = models.DateField(verbose_name=u'Дата окончания действия льготы', auto_now_add=True)
    description = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    periodicity = models.IntegerField(verbose_name=u'Периодичность', default=3, choices=PERIODICITY)
    group = models.ForeignKey(BenefitsType, verbose_name=u'Группа льготы', on_delete=models.CASCADE, null=False, blank=False)
    information_documents = models.ManyToManyField(InformationDocuments, blank=True)
    required_documents = models.ManyToManyField(RequiredDocuments, blank=True)



    def __str__(self):
        return '%s %s %s' % (self.title, self.value, self.periodicity)

    class Meta:

        verbose_name = u'Льгота'
        verbose_name_plural = u'Льготы'




class Requirement(models.Model):

    """
    Общий список всех требований
    """

    title = models.CharField(max_length=512, verbose_name=u'Заголовок')


    def __str__(self):
        return str(self.title)

    class Meta:

        verbose_name = u'Требование'
        verbose_name_plural = u'требования'



class RequirementsValue(models.Model):

    """
    Все возможные значения для требований
    """

    requirement = models.ForeignKey(Requirement, verbose_name=u'Требование', on_delete=models.CASCADE, null=False, blank=False)
    value = models.CharField(max_length=512, verbose_name=u'Значение')


    def __str__(self):
        return '%s %s' % (self.requirement, self.value)

    class Meta:

        verbose_name = u'Значение'
        verbose_name_plural = u'Значения требований'


class BenefitRequrements(models.Model):
    """
    Значение конкретного требования для конкретной льготы
    """

    requirement_value = models.ForeignKey(RequirementsValue, verbose_name=u'Необходимое значение для требования', on_delete=models.CASCADE, null=False, blank=False)
    benefit = models.ForeignKey(Benefit, verbose_name=u'Льгота', on_delete=models.CASCADE, null=False, blank=False)
    sign = models.IntegerField(verbose_name=u'Знак', default=3, choices=SIGN)


    class Meta:

        verbose_name = u'Необходимое значение требования'
        verbose_name_plural = u'Необходимые значения требований'
